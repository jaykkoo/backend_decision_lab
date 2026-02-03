resource "digitalocean_kubernetes_cluster" "k8s" {
  name    = var.cluster_name
  region  = var.region
  version = "1.29.1-do.0"

  node_pool {
    name       = "autoscale-pool"
    size       = var.node_size
    auto_scale = true
    min_nodes  = var.min_nodes
    max_nodes  = var.max_nodes
  }
}

resource "digitalocean_container_registry" "registry" {
  name                   = "myapp-registry"
  subscription_tier_slug = "basic"
}
