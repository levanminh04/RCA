args <- commandArgs(trailingOnly=TRUE)
source("D:/RCA-ext/work/T-014/CIRCA/circa/graph/r/causal.R")
cat("R", R.version.string, "pcalg", as.character(packageVersion("pcalg")), "\n")
cat("START: exact causal.R, alpha=.05, m.max=Inf, numCores=1; input full600\n")
for (stem in c("cartservice_cpu_1", "cartservice_mem_1")) {
  path <- paste0("D:/RCA-ext/work/T-014/audit-r/",stem,"_input.csv")
  d <- read.csv(path,check.names=FALSE)
  cat("PC_BEGIN", stem, nrow(d), ncol(d), "\n")
  flush.console()
  start <- proc.time()
  tryCatch({
    g <- runPC(as.matrix(d), CItest="gauss", alpha=.05, m.max=Inf, numCores=1)
    colnames(g) <- rownames(g) <- names(d)
    write.csv(g, paste0("D:/RCA-ext/work/T-014/audit-r/",stem,"_pcalg.csv"),row.names=FALSE)
    cat("PC_END", stem, "diagnostic_elapsed",(proc.time()-start)[["elapsed"]],"\n")
  }, error=function(e) cat("PC_ERROR",stem,conditionMessage(e),"\n"))
}
write.csv(as.data.frame(installed.packages()[,c("Package","Version","Built")]),
          "D:/RCA-flashticket/results/T-014/audit/r-packages-installed.csv",row.names=FALSE)
cat("DONE\n")
