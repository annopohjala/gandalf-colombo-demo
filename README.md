 Gandalf-Colombo-Demo 

## Links
- App IP: 16.16.83.217 (static Elastic IP)
- Gandalf: http://16.16.83.217/gandalf (image)
- Colombo Time: http://16.16.83.217/colombo (time in Asia/Colombo)
- Metrics: http://16.16.83.217/metrics (counters)
- Prometheus UI: http://13.60.70.83:9090 (scrape job 'gcd-app' – UP, graphs counters) 

## Decisions and Choices
- Language: Python/Flask (simple, from Flask Mega-Tutorial for basic routes/metrics).
- Cloud: AWS eu-north-1 (low latency from Estonia, free tier t3.micro).
- Kubernetes: K3s (lightweight, single-node for demo – no full K8s overhead).
- Exposure: hostPort 80 (direct bind to EC2 port 80 – only port 80 open in SG).
- Metrics: Two separate counters (as required), Prometheus client for export.
- Prometheus: Separate VM (as required), scrapes /metrics every 15s.
- Tagging: All resources tagged (Project=gandalf-colombo-demo, Expires=2025-12-31).
- Changes: Started with NodePort (30080), switched to hostPort to meet "only port 80 open" – removed service.yaml.

## Troubleshooting Notes
- K3s boot delays: Disabled Traefik, used --disable=traefik.
- Image pulls: `imagePullPolicy: Never` for local builds.


## Security Best Practices (Demo and Production Context)
For this demo, the app is public on port 80 (no sensitive data, per assignment needs). In production, restrict access to reduce attacks (e.g., DDoS, scraping). Here's how:

- **AWS Security Groups (Main Firewall – Best Practice)**: Limit inbound traffic to known IPs. Why? Blocks strangers; least privilege. How: AWS Console > Security Groups > Edit inbound > For HTTP (80), change Source from 0.0.0.0/0 to Prometheus IP (13.60.70.83/32). Save. Now only Prometheus can access /metrics.
- **VM Firewall (UFW – Extra Layer if Needed)**: Inside the VM, use ufw for host-level control. Why? Double protection if AWS group fails. How: On app VM: `sudo ufw enable; sudo ufw allow from 13.60.70.83 to any port 80`. Check `sudo ufw status`. (Not needed for demo, but production yes.)
- **Why These?**: AWS groups are cloud-native (best for EC2). UFW is simple OS-level. Together, they follow defense-in-depth (multiple layers). In context: Demo has public access for testing; production restricts to allowed IPs (e.g., Prometheus for /metrics, reviewers for app).

## Suggestions for Production Improvements

These are realistic next steps I would implement in a real environment:

## Suggestions for Production Improvements

These are realistic next steps I would implement in a real environment:

- **Ansible** – Replace manual SSH + bash with proper configuration management  
  → One command (`ansible-playbook site.yml`) configures both VMs automatically  
  → No copy-paste mistakes, fully reproducible

- **GitHub Actions** – Automatic checks on every push  
  → Lints Python code, runs tests, builds Docker image  
  → Catches bugs before they reach the servers

- **Ruff linter** – Fast Python code checker  
  → Finds bugs and formatting issues in seconds  
  → `pip install ruff && ruff check .`

- **Non-root container** – Security best practice  
  → App runs as normal user (UID 1000) instead of root  
  → Add to deployment.yaml:  
    ```yaml
    securityContext:
      runAsUser: 1000
      runAsGroup: 1000
	  
- **Grafana dashboard – Pretty graphs instead of raw Prometheus
  → 30-second setup: docker run -d -p 3000:3000 grafana/grafana
  → Connects to Prometheus → beautiful counter graphs


- **Restricted Prometheus UI – Currently open for review
  → In production: only allowed IPs via AWS security group + ufw
  → For this demo: I can whitelist your IP on request (just tell me)

Screenshots attached in submission.
