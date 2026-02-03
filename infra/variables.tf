variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "fra1"
}

variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
  default     = "bluegreen-cluster"
}

variable "node_size" {
  description = "Node size"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "min_nodes" {
  type    = number
  default = 2
}

variable "max_nodes" {
  type    = number
  default = 5
}
