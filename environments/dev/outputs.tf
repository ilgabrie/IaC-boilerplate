####################################################################################
# Output variables
####################################################################################
output "dataproc-network" {
 value = data.google_compute_network.dataproc_network.name
}
