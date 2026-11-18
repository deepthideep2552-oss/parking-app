# Parking Slot Booking System – DevOps CI/CD Assignment

A Flask web app for booking parking slots. It is deployed using **Docker** and an
automated **Jenkins CI/CD pipeline** that triggers whenever code is pushed to **GitHub**.

## Features

- 16 slots on 2 levels (A and B), with car and bike slots
- Live count of Total / Available / Booked slots
- Book a slot with vehicle number and owner name
- Prevents double booking of a slot and parking the same vehicle twice
- Release a slot with an automatic parking fee (Rs. 20 per hour, minimum 1 hour)
- Green slots are free and red slots are booked
- REST API: `/api/slots` and health check: `/health`
- 6 automated tests run by Jenkins on every build

## Project Structure

```
parking-app/
├── app.py              # Flask application (slot booking logic)
├── templates/
│   └── index.html      # Parking lot web page
├── test_app.py         # Automated tests (pytest)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Builds the Docker image
├── build-image.sh      # Shell script to build, test & run the image
├── docker-compose.yml  # YAML: run the app with Docker Compose
├── k8s/
│   ├── deployment.yaml # YAML: Kubernetes Deployment (2 pods)
│   └── service.yaml    # YAML: Kubernetes Service (port 30080)
├── .dockerignore
├── .gitignore
├── .gitattributes      # Keeps .sh files with Linux line endings
├── Jenkinsfile         # CI/CD pipeline definition
└── README.md
```

## Pipeline Flow

```
Developer --git push--> GitHub --(Poll SCM / webhook)--> Jenkins
   Jenkins: Checkout -> Build Docker Image -> Run Tests -> Deploy Container
   Result:  App running at http://localhost:5000
```

---

## STEP 1 – Install Required Software

| Software | Download | Check it works |
|---|---|---|
| Docker Desktop | https://www.docker.com/products/docker-desktop | `docker --version` |
| Git | https://git-scm.com/downloads | `git --version` |
| Java JDK 21 (needed by Jenkins) | https://adoptium.net | `java -version` |
| Jenkins (LTS) | https://www.jenkins.io/download | open http://localhost:8080 |

**Docker Desktop notes (Windows):** enable WSL 2 when the installer asks, restart the PC,
then open Docker Desktop and wait until it shows **"Engine running"**.

📸 *Screenshot: Docker Desktop dashboard, and `docker --version`, `git --version`, `java -version` output.*

---

## STEP 2 – Practise Docker Commands

Open Command Prompt / PowerShell inside the `parking-app` folder.

```bash
docker --version                         # Docker version
docker info                              # Docker system details
docker pull hello-world                  # Download an image
docker run hello-world                   # Run a test container
docker images                            # List images

docker build -t parking-app .            # Build image from Dockerfile
docker run -d --name myapp -p 5000:5000 parking-app   # Run container in background
docker ps                                # List running containers
docker ps -a                             # List all containers
docker logs myapp                        # View container logs
docker exec -it myapp sh                 # Open a shell inside container (type 'exit' to leave)
docker stop myapp                        # Stop container
docker start myapp                       # Start it again
docker rm -f myapp                       # Remove container
docker rmi hello-world                   # Remove an image
docker system df                         # Disk usage by Docker
```

Open **http://localhost:5000** in the browser after `docker run` to see the app.

📸 *Screenshot: output of each command and the app running in the browser.*

---

## STEP 2A – Build the Image with the Shell Script

`build-image.sh` checks that Docker is running, builds the image with a version tag
and the `latest` tag, runs the tests inside the image, lists the images, and can
start the container.

On Windows, open **Git Bash** in the project folder. Git Bash is installed with Git.

```bash
chmod +x build-image.sh          # make the script executable (once)
./build-image.sh                 # build with a date-time version tag
./build-image.sh v1.0            # build with version tag v1.0
./build-image.sh v1.0 --run      # build, test and run at http://localhost:5000
docker images parking-app        # see all versions of the image
```

📸 *Screenshot: script output showing all steps and SUCCESS, and the `docker images` list.*

---

## STEP 2B – YAML Files and Commands

### a) Docker Compose (`docker-compose.yml`)

```bash
docker compose config            # validate & display the YAML
docker compose up -d --build     # build image and start the app in background
docker compose ps                # list compose containers
docker compose logs              # view logs
docker compose stop              # stop the containers
docker compose start             # start them again
docker compose down              # stop and remove the containers
```

The app runs at **http://localhost:5001**. Port 5000 is kept free for the Jenkins deployment.

### b) Kubernetes (`k8s/deployment.yaml`, `k8s/service.yaml`)

First enable Kubernetes: **Docker Desktop → Settings → Kubernetes → Enable Kubernetes → Apply & Restart**.
Wait until Kubernetes shows as running.

```bash
kubectl version                          # check kubectl works
kubectl get nodes                        # should show docker-desktop as Ready
./build-image.sh v1.0                    # make sure image parking-app:latest exists

kubectl apply -f k8s/                    # create Deployment + Service from YAML
kubectl get deployments                  # see the deployment (2/2 ready)
kubectl get pods                         # see the 2 running pods
kubectl get services                     # see parking-app-service on port 30080
kubectl describe deployment parking-app  # full details
kubectl logs -l app=parking-app          # logs from the pods

kubectl scale deployment parking-app --replicas=4   # scale up to 4 pods
kubectl get pods                                     # now 4 pods

kubectl delete -f k8s/                   # remove everything created by the YAML
```

The app runs at **http://localhost:30080**.

> **If the pods show `ErrImageNeverPull`:** Kubernetes can't see your local image.
> In Docker Desktop, set **Settings → Kubernetes → Cluster provisioning** to **kubeadm**,
> or use Docker Compose instead.

📸 *Screenshot: each command's output and the app at ports 5001 and 30080.*

---

## STEP 3 – Practise Git Commands & Push to GitHub

1. Create a free account on https://github.com and create a **new public repository**
   named `parking-app` (do **not** add a README there).
2. In the `parking-app` folder run:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git init                                  # Create local repository
git status                                # See changed files
git add .                                 # Stage all files
git commit -m "Initial commit: parking app with Dockerfile and Jenkinsfile"
git branch -M main                        # Rename branch to main
git remote add origin https://github.com/<your-username>/parking-app.git
git push -u origin main                   # Push code to GitHub

git log --oneline                         # Commit history
git branch                                # List branches
git checkout -b feature-test              # Create & switch to a new branch
git checkout main                         # Switch back
git merge feature-test                    # Merge branch
git pull                                  # Get latest changes from GitHub
git diff                                  # Show unstaged changes
```

📸 *Screenshot: each command's output and the GitHub repo page showing your files.*

---

## STEP 4 – Set Up Jenkins

1. Open **http://localhost:8080**.
2. Unlock Jenkins with the initial admin password. Its file path is shown on the screen, e.g.
   `C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword`.
3. Click **Install suggested plugins**. This includes Git and Pipeline.
4. Create the admin user and finish setup.
5. Make sure Jenkins can use Docker: open Command Prompt and check `docker ps` works.
   On Windows, Docker Desktop is installed for one user, so the Jenkinsfile adds Docker's
   folder (`DOCKER_BIN`) to the PATH. Change `DOCKER_BIN` if Docker is installed elsewhere.
   Docker Desktop must be open while Jenkins builds.
   On Linux, run `sudo usermod -aG docker jenkins` and restart Jenkins.

📸 *Screenshot: Unlock screen, plugin installation, Jenkins dashboard.*

---

## STEP 5 – Create the Pipeline (Pipeline script from SCM)

1. Jenkins Dashboard → **New Item** → name: `parking-app-pipeline` → choose **Pipeline** → OK.
2. Under **Triggers / Build Triggers**, tick **Poll SCM** and enter `H/2 * * * *`.
   The Jenkinsfile also sets this.
3. Scroll to **Pipeline** section:
   - **Definition:** `Pipeline script from SCM`
   - **SCM:** `Git`
   - **Repository URL:** `https://github.com/<your-username>/parking-app.git`
   - **Branch Specifier:** `*/main`
   - **Script Path:** `Jenkinsfile`
4. Click **Save**, then **Build Now** for the first build.
5. Open the build → **Console Output** to see each stage.
   Open **Stage View** to see the stages turn green.
6. Visit **http://localhost:5000**. The app is deployed by Jenkins.

📸 *Screenshot: pipeline configuration page, Stage View, Console Output, the app in the browser.*

---

## STEP 6 – Prove Automatic CI/CD Trigger on Push

1. Make a small change, e.g. in `app.py` change the parking rate:
   `RATE_PER_HOUR = 20` to `RATE_PER_HOUR = 30`.
2. Push it:

```bash
git add .
git commit -m "Update parking rate to Rs. 30 per hour"
git push
```

3. Within about 2 minutes Jenkins starts a **new build automatically** without clicking Build Now.
   The build page shows *"Started by an SCM change"*.
4. Refresh http://localhost:5000. The header now shows **Rate: Rs. 30 / hour**.

📸 *Screenshot: git push output, the new build with "Started by an SCM change", the updated app page.*

> **Optional – instant trigger with a GitHub webhook:** GitHub can't reach `localhost`,
> so expose Jenkins with **ngrok** (`ngrok http 8080`). In GitHub go to
> **Repo → Settings → Webhooks → Add webhook** and set the Payload URL to
> `https://<ngrok-url>/github-webhook/` with content type `application/json`.
> In Jenkins, tick **GitHub hook trigger for GITScm polling**.

---

## STEP 7 – Screenshot Checklist for Printout

- [ ] Docker Desktop installed and running
- [ ] `docker --version`, `git --version`, `java -version`
- [ ] All Docker commands (Step 2) with output
- [ ] Shell script `build-image.sh` output (Step 2A)
- [ ] Docker Compose commands and app at port 5001 (Step 2B)
- [ ] Kubernetes `kubectl` commands, pods running, app at port 30080 (Step 2B)
- [ ] All Git commands (Step 3) with output
- [ ] GitHub repository showing Dockerfile and Jenkinsfile
- [ ] Jenkins dashboard
- [ ] Pipeline configuration (Pipeline script from SCM)
- [ ] Successful build: Stage View, all stages green
- [ ] Console Output
- [ ] App running at http://localhost:5000
- [ ] Code change + `git push`
- [ ] Auto-triggered build ("Started by an SCM change")
- [ ] Updated app after auto deployment
- [ ] `docker ps` showing `parking-app-container` running

Print the screenshots with a short caption under each one and put them in the transparent file.

---

## Run Locally Without Docker (optional)

```bash
pip install -r requirements.txt
python -m pytest -v
python app.py
```
