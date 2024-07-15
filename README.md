# CAP Application combined with Python

This is a sample project combining a CAP application with a Python application. It's target runtime is the SAP Business Technology Platform (BTP) Kyma environment.

It contains these folders and files, following our recommended project layout:

| File or Folder | Purpose                              |
| -------------- | ------------------------------------ |
| `app/`         | content for UI frontends goes here   |
| `chart/`       | HELM Charts                          |
| `db/`          | your domain models and data go here  |
| `srv/`         | your service models and code go here |
| `srv-python/`  | The Python application go here       |
| `package.json` | project metadata and configuration   |
| `readme.md`    | this getting started guide           |

## Preconditions

- BTP Subaccount with Kyma Runtime
- BTP Subaccount with Cloud Foundry Space
- HANA Cloud instance available for your Cloud Foundry space
- BTP Entitlements for: _HANA HDI Services & Container_ plan _hdi-shared_
- Container Registry
- Command Line Tools: `kubectl`, `kubectl-oidc_login`, `pack`, `docker`, `helm`, `cf`
- Logged into Kyma Runtime (with `kubectl` CLI), Cloud Foundry space (with `cf` CLI) and Container Registry (with `docker login`)
- `@sap/cds-dk` >= 6.6.0

## Local Development

To run the application locally, you need to start the CAP application and the Python application. To work directly with the HANA Cloud instance you need to connect to the Cloud Foundry Environment:

```bash
cf login --sso
```

then you can deploy with:

```bash
cds deploy --to hana
```

To run the CAP application you need to start the CAP application with:

```bash
cds watch --profile hybrid --auto-undeploy
```

To run the Python application you need to start the Python application with:

```bash
npm run start:python
```

## Prepare Kubernetes Namespace

1. Export the kubeconfig.yaml

   ```
   export KUBECONFIG=~/.kube/cap-kyma-app-config
   ```

2. Setting the namespace

   ```
   kubectl config set-context --current --namespace=<<NAMESPACE>>
   ```

## Debug deployment

```bash
kubectl get pods
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```
