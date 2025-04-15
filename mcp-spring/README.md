MCP Spring
==========

This repository contains a sample Spring AI MCP Server that runs on ECS; which is used by a Spring AI Agent using Bedrock; which also runs on ECS and is exposed publicly via a Load Balancer.

Keywords
---------

- Spring AI
- Model Context Protocol (MCP)
- Amazon Bedrock
- Amazon Elastic Container Service (ECS)
- Kotlin

Architecture
------------

```mermaid
flowchart LR
    subgraph aws[AWS]
        alb[Application Load Balancer]

        subgraph vpc[VPC]
            server[MCP Server\nECS Service]
            client[MCP Client / Bedrock Agent\nECS Service]
        end

        subgraph services[AWS Services]
            bedrock[Bedrock]
        end
    end

    internet((Internet))

    %% Connections
    internet <--> alb
    alb --> client
    client <--> bedrock
    client <--> server

    %% Styling
    style aws fill:#f5f5f5,stroke:#232F3E,stroke-width:2px
    style vpc fill:#E8F4FA,stroke:#147EBA,stroke-width:2px
    style services fill:#E8F4FA,stroke:#147EBA,stroke-width:2px

    style alb fill:#FF9900,color:#fff,stroke:#FF9900
    style server fill:#2196f3,color:#fff,stroke:#2196f3
    style client fill:#2196f3,color:#fff,stroke:#2196f3
    style bedrock fill:#FF9900,color:#fff,stroke:#FF9900
    style internet fill:#fff,stroke:#666,stroke-width:2px

    %% Link styling
    linkStyle default stroke:#666,stroke-width:2px
```

References
----------

- Running MCP-Based Agents (Clients & Servers) on AWS, _https://community.aws/content/2v8AETAkyvPp9RVKC4YChncaEbs/running-mcp-based-agents-clients-servers-on-aws_
- Sample: MCP Agent with Spring AI and Bedrock, _https://github.com/aws-samples/Sample-Model-Context-Protocol-Demos/tree/main/modules/spring-ai-agent-ecs_
