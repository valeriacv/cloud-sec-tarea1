from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDSInstance
from diagrams.aws.network import CloudFront
from diagrams.aws.network import APIGateway
from diagrams.aws.blockchain import Blockchain
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import PV
from diagrams.k8s.infra import Node
from diagrams.k8s.network import Ingress

with Diagram("Arquitectura Omnione OpenDID", show=False):  
    with Cluster("VCP"):
        mailService = SimpleEmailServiceSes("Mail Service")
        nodeN = Node("Node n")
        node1 = Node("Node 01")

        node1 >> Edge(style="dashed", color="black") >> nodeN
        nodeN >> Edge(style="invis") >> mailService

        with Cluster("Database Layer"):
            fabric = Blockchain("HyperLedger Fabric")
            db = RDSInstance("PostgreSQL")

        with Cluster("Application Layer"):
            with Cluster("external-services-ns"):
                externalNS = Pod("Notification service")

            with Cluster("trusted-ns", direction="LR"):
                agent = Pod("Trust agent")
                trustedNS = Pod("Trusted Notification Service")

                agent >> Edge(style="invis") >> trustedNS
            
            with Cluster(""):
                apiMiddleware = Pod("Legacy API middleware")

            with Cluster("wallet-services-ns"):
                wallet = Pod("Wallet service")
                CApp = Pod("CApp service")
                user = Pod("User service")
                certificateVol = PV("Certificate Volumen")
                wallet >> Edge(style="invis") >> CApp >> Edge(style="invis") >> user

            ing = Ingress("Ingress")
            ing >> CApp

            with Cluster("issuer-services-ns"):
                issuer = Pod("Issuer service")

            with Cluster("verifier-services-ns"):
                verifier = Pod("Verifier service")

            verifier >> Edge(style="invis") >> apiMiddleware
            issuer >> Edge(style="invis") >> apiMiddleware

            apiMiddleware >> Edge(style="invis") >> externalNS
            apiMiddleware >> Edge(style="invis") >> trustedNS
            verifier >> Edge(style="invis") >> trustedNS
            user >> Edge(style="invis") >>  externalNS

        with Cluster("Presentation Layer"):
            cloudfront = CloudFront("Amazon CloudFront")
            waf = Custom("Amazon Web Application Firewall", "./img/waf.png") 
            apigateway = APIGateway("Amazon API Gateway")

            cloudfront >> Edge(style="invis") >> waf

            presentationLayer = [cloudfront, apigateway]
           
        k8 = Custom("K8", "./img/k8.png")

        presentationLayer  >> Edge(style="invis") >> k8
        k8  >> Edge(style="invis") >> wallet
    with Cluster("Legacy Layer"):
        legacy1 = Custom("Legacy Service 1", "./img/legacy.png")
        legacy2 = Custom("Legacy Service 2", "./img/legacy.png")

        legacy1 >> Edge(style="invis") >> legacy2

    dnsZones = [Custom("DNS Zones", "./img/dns.png"),
                Custom("DNS Zones", "./img/dns.png"),
                Custom("DNS Zones", "./img/dns.png")]

    dnsPolicy = Custom("DNS Security Policy", "./img/dns_policy.png")
    dnsPolicy >> Edge(style="invis") >> dnsZones
       
    
    externalNS >> Edge(style="invis") >> db
    waf >> Edge(style="invis") >> verifier
    waf >> Edge(style="invis") >> wallet
    dnsZones >> Edge(style="invis") >> presentationLayer[0]
    wallet >> Edge(color="black", style="dashed")  >> issuer 
    wallet >> Edge(color="black", style="dashed")  >> verifier 
