<h1 align="left">
  <img src="https://argo-cd.readthedocs.io/en/stable/assets/logo.png" 
       alt="ArgoCD" width="60" style="vertical-align:middle; margin-right:10px;">
  CI/CD com o Github Actions e ArgoCD
</h1>

![ARGOCD](https://img.shields.io/badge/Argo%20CD-1e0b3e?style=for-the-badge&logo=argo&logoColor=#d16044)  ![KUBERNETES](https://img.shields.io/badge/Kubernetes-3069DE?style=for-the-badge&logo=kubernetes&logoColor=white) ![DOCKER](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![GITHUBACTIONS](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)


Este repositório tem como objetivo documentar a aplicação, incluindo instruções sobre execução local, build, testes e integração com o pipeline de CI/CD utilizado para o deploy de uma aplicação FastAPI.
O projeto faz parte de um fluxo de automação implementado com GitHub Actions, Docker e ArgoCD.

---
<br>
<br>

**Requisitos**

Antes de começar, você precisará de:

- Conta no GitHub (com repositórios públicos)

- Conta no Docker (com token de acesso)

- kubectl configurado corretamente (kubectl get nodes)

- ArgoCD instalado no cluster local

- Git instalado

- Python 3 e Docker funcionando

<br>
<br>
<br>
<br>

**Estrutura do Projeto**

O projeto é dividido em dois repositórios GitHub:

🗂️ Repositório 1 — hello-app

Contém:

- Código da aplicação FastAPI

- Arquivo Dockerfile

- Dependências em requirements.txt

- Workflow do GitHub Actions (CI/CD)

<br>
Como fazer: 

Em uma pasta no seu PC, clone este repositório e dê um push no seu repositório:

```bash
cd C:\usuarios\<seu-nome>\hello-app
git clone https://<Seu-repositorio-hello-app>
git remote add origin http://<Seu-repositorio-hello-app>
git add .
git commit -m "Clonando repositório"
git push origin main
```

<br>
<br>

🗂️ Repositório 2 — hello-manifests

- Armazena os manifestos do Kubernetes usados pelo ArgoCD:

- deployment.yaml

- service.yaml

<br>
Como fazer: 

E em outra pasta, clone o repositório: https://github.com/RayaneValadares/hello-manifests

```bash
cd C:\usuarios\<seu-nome>\hello-manifests
git clone https://github.com/RayaneValadares/hello-manifests
git remote add origin http://<Seu-repositorio-hello-manifests>
git add .
git commit -m "Clonando repositório"
git push origin main
```

Precisamos criar também um repositório público no Docker:

```bash
usuario-docker/main-python
```
Pode deixá-lo vazio.

<br>
<br>
<br>
<br>

**Estrutura de Arquivos**
```bash
📦 hello-app/
┣ 📜 main.py
┣ 📜 requirements.txt
┣ 📜 Dockerfile
┗ 📜 .github/workflows/post.yaml
```

<br>
<br>
<br>
<br>

**Configuração das Secrets do GitHub**

O arquivo de workflow usa variáveis seguras (secrets) para login no Docker Hub e autenticação via SSH.
Siga os passos abaixo para configurá-las.

1️⃣ Gerar Chaves SSH

- No PowerShell, crie uma chave SSH (caso ainda não tenha):
```bash
ssh-keygen -t ed25519 -C "seu_email@exemplo.com"
```

- Exiba a chave pública:
```bash
cat .\id_ed25519.pub
```

- Exiba a chave privada:
```bash
cat .\id_ed25519
```

- A pública será algo como:
```bash
ssh-ed25519 AAAA123abc... seuemail@exemplo.com
```
<br>

2️⃣ Adicionar a chave no GitHub

- Vá em Settings > SSH and GPG keys > New SSH key

- Dê um nome e cole sua chave pública

<br>

3️⃣ Criar Secrets no Repositório

- No repositório hello-app, acesse:
Settings > Secrets and variables > Actions > New repository secret

- Crie as seguintes secrets:

| Nome | Descrição |
|-------------|------------|
| **DOCKER_USERNAME** |	Seu nome de usuário do Docker Hub |
| **DOCKER_PASSWORD** | Seu token de acesso ou senha do Docker Hub |
| **SSH_PRIVATE_KEY** | Chave privada gerada anteriormente |


Com isso, o GitHub Actions poderá fazer login no Docker e atualizar o repositório de manifests automaticamente.

Imagem do DockerHub e atualizações:
![alt text](<Captura de tela 2025-11-07 180408.png>)

<br>

Imagem do Repositório hello-manifests atualizado com ultima imagem lançada:

![alt text](<Captura de tela 2025-11-07 180643.png>)

<br>
<br>
<br>
<br>

**Funcionamento do Workflow (deployment.yaml)**

O pipeline executa automaticamente sempre que há commit na branch main.
As etapas são:

1️⃣ Build da imagem Docker da aplicação FastAPI

2️⃣ Push da imagem para o Docker Hub

3️⃣ Atualização automática do repositório hello-manifests com a nova tag da imagem

4️⃣ O ArgoCD detecta a mudança e aplica o novo deploy no Kubernetes

<br>
<br>
<br>
<br>

**Configuração do ArgoCD**

Abra o Docker Desktop e execute no Terminal:

```bash
kubectl create namespace argocd
```
![alt text](<Captura de tela 2025-11-06 153832.png>)

Instale o ArgoCD:
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Verifique se os serviços foram criados:
```bash
kubectl get svc -n argocd
```

Crie um túnel local para acessar o painel:
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
![alt text](<Captura de tela 2025-11-06 153816.png>)

Em outro terminal, recupere a senha inicial:

```bash
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}")))
```

Acesse:
👉 http://localhost:8080

![alt text](image.png)

Usuário: admin

Senha: (a obtida no comando anterior)


<br>
<br>
<br>
<br>

**Criar Aplicação no ArgoCD**

- Vá em Applications → + NEW APP

- Configure os campos:

| Campo | Valor |
|-------------|------------|
| **Application Name** |	hello-app |
| **Project Name** | default |
| **Repository URL** | (o seu repositório conectado) |
| **Revision** |	HEAD |
| **Path** | . |
| **Cluster** |	in-cluster |
| **Namespace** | default |

Clique em CREATE.

![alt text](<Captura de tela 2025-11-06 161951.png>)

<br>
<br>
<br>
<br>

**Sincronizar a Aplicação**

Abra a aplicação criada e clique em SYNC → SYNCHRONIZE. O ArgoCD fará o deploy automático de todos os recursos definidos no manifest.

Aguarde até o status mudar para Healthy e Synced ✅

![alt text](<Captura de tela 2025-11-06 153350.png>)

<br>
<br>
<br>
<br>

**Testando a Aplicação**

Execute o port-forward para acessar a aplicação:

```bash
kubectl port-forward svc/hello-app 8080:80
```
<br>

Acesse no navegador:
http://localhost:8080

![alt text](<Captura de tela 2025-11-06 161742.png>)

<br>
<br>
<br>
<br>

**Conclusão**

Parabéns! 🎊
Você acabou de configurar um pipeline CI/CD completo com GitHub Actions, Docker Hub e ArgoCD.
A cada novo commit, a aplicação será reconstruída, publicada e atualizada automaticamente no Kubernetes local.
