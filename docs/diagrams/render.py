"""Render the EKS portfolio SVGs and Mermaid sketches. Python standard library only.

Edit diagram definitions below, then run: python3 diagrams/render.py
The SVGs are arranged for reading; Mermaid preserves their labeled relationships.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent
INK = '#172b35'
MUTED = '#475569'
COLORS = {
    'neutral': ('#f8fafc', '#94a3b8'),
    'compute': ('#eff6ff', '#2563eb'),
    'identity': ('#f5f3ff', '#7c3aed'),
    'data': ('#ecfdf5', '#047857'),
    'network': ('#fff7ed', '#c2410c'),
}

class Diagram:
    def __init__(self, name, title, subtitle, height):
        self.name, self.height = name, height
        self.nodes, self.edges = [], []
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#64748b"/></marker></defs>',
                      '<style>text{font-family:Arial,Helvetica,sans-serif} .edge{fill:none;stroke:#64748b;stroke-width:2;marker-end:url(#arrow)}</style>',
                      f'<rect width="1200" height="{height}" fill="white"/>']
        self.text(40, 42, 'EKS COMPUTE OPERATIONS LAB  /  JADEN RAZO', 13, '#475569', True)
        self.text(40, 88, title, 32, INK, True)
        self.text(40, 119, subtitle, 16)

    def text(self, x, y, value, size=16, color=MUTED, bold=False, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')

    def rect(self, x, y, w, h, fill='#f8fafc', stroke='#cbd5e1'):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}"/>')

    def banner(self, y, title, detail, kind='neutral'):
        fill, stroke = COLORS[kind]
        self.rect(40, y, 1120, 74, fill, stroke)
        self.text(60, y+29, title, 18, INK, True)
        self.text(60, y+54, detail, 16)

    def section(self, y, title):
        self.text(40, y, title, 16, INK, True)

    def node(self, key, x, y, w, h, title, lines, kind='neutral'):
        fill, stroke = COLORS[kind]
        self.rect(x,y,w,h,fill,stroke)
        self.text(x+18,y+29,title,19,INK,True)
        for i,line in enumerate(lines):
            self.text(x+18,y+55+i*22,line,15)
        self.nodes.append((key,title,lines,kind))
        return (x,y,w,h)

    def edge(self, a, b, label, boxes):
        x,y,w,h = boxes[a]; xx,yy,ww,hh = boxes[b]
        self.parts.append(f'<path class="edge" d="M{x+w+3} {y+h/2} H{xx-5}"/>')
        self.edges.append((a,b,label))

    def save(self):
        self.parts.append('</svg>')
        (OUT/(self.name+'.svg')).write_text('\n'.join(self.parts)+'\n', encoding='utf-8')
        m = ['flowchart LR']
        for key,title,lines,kind in self.nodes:
            label = '<br/>'.join([title]+lines).replace('"', '&quot;')
            m.append(f'  {key}["{label}"]:::{kind}')
        for a,b,label in self.edges:
            m.append(f'  {a} -->|"{label}"| {b}')
        for kind,(fill,stroke) in COLORS.items():
            m.append(f'  classDef {kind} fill:{fill},stroke:{stroke},color:{INK}')
        (OUT/(self.name+'.mmd')).write_text('\n'.join(m)+'\n',encoding='utf-8')

def compute():
    d=Diagram('eks-compute-architecture','One workload, two EKS compute models',
              'Historical deployment view | us-east-1 | EC2 and Fargate were exercised in separate cluster phases.',1380)
    d.banner(145,'Deployment lifecycle: EC2 phase → teardown → Fargate phase → teardown',
             'Both lab clusters and the lab NAT gateway were removed. This diagram does not show a live deployment.','network')
    b={}
    d.section(260,'01  MANAGEMENT ACCESS — repeated for each cluster')
    b['ops']=d.node('ops',40,280,330,100,'OpsBox EC2',['eksctl + kubectl','Separate VPC; public API access'])
    b['api']=d.node('api',435,280,330,100,'EKS API / control plane',['AWS-managed control plane','Public + private endpoints'],'compute')
    b['logs']=d.node('logs',830,280,330,100,'CloudWatch Logs',['Audit + authenticator logs','Configured retention: one day'],'data')
    d.edge('ops','api','management API',b); d.edge('api','logs','control-plane logs',b)
    d.text(40,408,'Public endpoint allowlist: OpsBox egress /32. Private endpoints serve connectivity inside the lab VPC.',15)

    d.section(455,'02  EC2 PHASE — two t3.medium managed workers in private subnets')
    b['eo']=d.node('eo',40,477,330,112,'Service observer',['Internal HTTP probes','GET /readyz; timestamped OK / FAIL'])
    b['es']=d.node('es',435,477,330,112,'inventory-status Service',['Namespace: ops-lab','ClusterIP; selects application Pods'],'compute')
    b['ep']=d.node('ep',830,477,330,112,'Application: two replicas',['Scheduled on the EC2 worker pool','Non-root; readiness + liveness'],'compute')
    d.edge('eo','es','HTTP request',b);d.edge('es','ep','eligible backend',b)
    d.text(40,618,'Exercises: broken readiness, Service selector mismatch, and node drain with a PodDisruptionBudget.',15)
    d.text(40,641,'Observed limitation: replicas were co-located during maintenance; two nodes did not guarantee replica spread.',15)

    d.section(694,'03  FARGATE PHASE — profile-selected Pods in private subnets')
    b['fo']=d.node('fo',40,716,330,112,'Service observer',['Internal HTTP probes','Scheduled on Fargate'])
    b['fs']=d.node('fs',435,716,330,112,'inventory-status Service',['Same application access pattern','ClusterIP; selects application Pods'],'compute')
    b['fp']=d.node('fp',830,716,330,112,'Application: two replicas',['Profile namespace: ops-lab','Required label: compute=lab'],'compute')
    d.edge('fo','fs','HTTP request',b);d.edge('fs','fp','eligible backend',b)
    d.text(40,857,'A separate system profile selected kube-system. Profile mismatch blocked new application Pod placement.',15)
    d.text(40,880,'Two configured private subnets do not establish that application replicas were evenly distributed across AZs.',15)

    d.section(933,'04  SHARED DEPLOYMENT NETWORK — outbound path, separate from the internal Service request')
    b['priv']=d.node('priv',40,955,250,100,'Private subnets',['10.80.10.0/24 · AZ a','10.80.11.0/24 · AZ b'],'network')
    b['nat']=d.node('nat',330,955,250,100,'One zonal NAT',['Public subnet in AZ a','10.80.0.0/24'],'network')
    b['igw']=d.node('igw',620,955,250,100,'Internet gateway',['Lab VPC: 10.80.0.0/16','Public subnet default route'],'network')
    b['ext']=d.node('ext',910,955,250,100,'Public endpoints',['Image registries and','required AWS endpoints'])
    d.edge('priv','nat','default route',b);d.edge('nat','igw','outbound',b);d.edge('igw','ext','outbound',b)
    d.text(40,1084,'A second public subnet (10.80.1.0/24, AZ b) existed. One NAT was a lab cost / availability tradeoff.',15)

    d.section(1136,'05  WORKLOAD ACCESS AUDIT — exercised on both compute models')
    b['sa']=d.node('sa',40,1158,330,100,'aws-audit Pod / account',['ServiceAccount: ops-lab/aws-audit','Projected identity token'],'identity')
    b['irsa']=d.node('irsa',435,1158,330,100,'IAM role through IRSA',['Cluster-specific OIDC trust','Role credentials for the workload'],'identity')
    b['s3']=d.node('s3',830,1158,330,100,'Synthetic S3 fixtures',['allowed/* reads permitted','Unrelated reads + writes denied'],'data')
    d.edge('sa','irsa','STS web identity',b);d.edge('irsa','s3','S3 authorization',b)
    d.text(40,1290,'Fargate Pod execution role: infrastructure duties. Workload S3 access: separate IRSA role.',15)
    d.text(40,1345,'SCOPE: independent lab • logical paths; return traffic omitted • resource IDs and account IDs omitted',13)
    d.save()

def state():
    d=Diagram('terraform-state-architecture','Terraform ownership and state access',
              'Retained infrastructure | two Terraform roots | separate state and lock objects in one S3 bucket.',1260)
    d.banner(145,'Current administrator exception: the OpsBox role still has AdministratorAccess',
             'Assuming a narrower network-backend role scopes that session; it does not remove direct administrator access.','network')
    b={}
    d.section(262,'01  NETWORK BACKEND — a dedicated role for state access')
    b['nr']=d.node('nr',40,285,330,120,'terraform/network',['Backend assumes the state role','Network resources use the provider'])
    b['role']=d.node('role',435,285,330,120,'eks-lab-terraform-state',['Trusts the OpsBox role','State: Get / Put; lock: Get / Put / Delete'],'identity')
    b['ns']=d.node('ns',830,285,330,120,'Network state in S3',['network/terraform.tfstate','network/terraform.tfstate.tflock'],'data')
    d.edge('nr','role','backend AssumeRole',b);d.edge('role','ns','scoped object access',b)
    d.text(40,435,'Policy simulations: state deletion and unrelated-object Get / Put were implicitly denied for the state role.',15)

    d.section(485,'02  NETWORK PROVIDER — infrastructure operations retain OpsBox credentials')
    b['np']=d.node('np',40,507,330,114,'AWS provider on OpsBox',['Used by terraform/network','AdministratorAccess remains'],'identity')
    b['net']=d.node('net',435,507,725,114,'14 imported network resources',['VPC, four subnets, internet gateway, three route tables,','public default route, and four subnet associations.'],'network')
    d.edge('np','net','AWS provider operations',b)
    d.text(40,651,'Retained network: private NAT default routes removed; no NAT or EKS cluster is managed by these roots.',15)

    d.section(701,'03  BOOTSTRAP ROOT — retained resources supporting Terraform itself')
    b['br']=d.node('br',40,723,330,114,'terraform/bootstrap',['AWS provider uses OpsBox role','Imports preserve existing settings'])
    b['boot']=d.node('boot',435,723,725,114,'Nine imported bootstrap resources',['Bucket + five S3 configuration resources;','network-backend IAM role, policy, and their attachment.'],'data')
    d.edge('br','boot','AWS provider operations',b)

    d.section(889,'04  BOOTSTRAP BACKEND — a separate key, accessed with OpsBox credentials')
    b['bb']=d.node('bb',40,911,330,114,'Bootstrap backend',['Uses OpsBox credentials directly','Local state migrated to S3'],'identity')
    b['bs']=d.node('bs',435,911,725,114,'Bootstrap state in the same S3 bucket',['bootstrap/terraform.tfstate','bootstrap/terraform.tfstate.tflock'],'data')
    d.edge('bb','bs','state + lock access',b)
    d.banner(1061,'Bucket controls: versioning · AES256 · Block Public Access · HTTPS-only policy',
             'SSE-C uploads blocked; BucketOwnerEnforced. Each backend enables native S3 state locking.','data')
    d.text(40,1171,'Lifecycle: bootstrap manages its own state bucket. Retain it during lab cleanup; recovery restoration is untested.',15)
    d.text(40,1196,'Terraform prevent_destroy guards the configured bucket resource; it does not block AWS administrator actions.',15)
    d.text(40,1231,'OWNERSHIP: EKS = eksctl • workload objects = Kubernetes manifests • retained network and backend = Terraform',13)
    d.save()

if __name__ == '__main__':
    compute()
    state()
    print('Rendered two SVG diagrams and two Mermaid topology sketches.')
