# Original causal.R, unchanged; all 25 predeclared MEM cases; no label to PC.
source('D:/RCA-ext/work/T-014/CIRCA/circa/graph/r/causal.R')
root <- 'D:/RCA-ext/work/T-014/audit-r/mem-target/'
inputs <- read.csv(paste0(root,'inputs.csv'),check.names=FALSE)
cat('START',R.version.string,'pcalg',as.character(packageVersion('pcalg')),'alpha .05 m.max Inf numCores 1; input full600\n')
results <- list()
batch <- proc.time()[['elapsed']]
for (index in seq_len(nrow(inputs))) {
  if (proc.time()[['elapsed']]-batch>840) {
    cat('BUDGET_STOP',index,'before case; audit method budget <=15min\n')
    break
  }
  stem <- inputs$stem[index]
  cat('PC_BEGIN',index,nrow(inputs),stem,as.character(Sys.time()),'\n');flush.console()
  start <- proc.time()[['elapsed']]
  result <- tryCatch({
    d <- read.csv(inputs$input[index],check.names=FALSE)
    if (stem=='cartservice_mem_1') {
      old <- read.csv('D:/RCA-ext/work/T-014/audit-r/cartservice_mem_1_input.csv',check.names=FALSE)
      stopifnot(identical(d,old))
      g <- as.matrix(read.csv('D:/RCA-ext/work/T-014/audit-r/cartservice_mem_1_pcalg.csv',check.names=FALSE))
      mode <- 'reuse_checked_input'
    } else {
      g <- runPC(as.matrix(d),CItest='gauss',alpha=.05,m.max=Inf,numCores=1)
      colnames(g) <- rownames(g) <- names(d)
      mode <- 'new_configuration_b'
    }
    write.csv(g,paste0(root,stem,'_pcalg.csv'),row.names=FALSE)
    list(stem=stem,status='ok',mode=mode,rows=nrow(d),columns=ncol(d),edges=sum(g!=0),
         diagnostic_elapsed=proc.time()[['elapsed']]-start,error='')
  },error=function(e) list(stem=stem,status='error',mode='no_fallback',rows=NA,columns=NA,edges=NA,
                           diagnostic_elapsed=proc.time()[['elapsed']]-start,error=conditionMessage(e)))
  results[[length(results)+1]] <- result
  write.csv(do.call(rbind,lapply(results,as.data.frame)),paste0(root,'pc-status.csv'),row.names=FALSE)
  cat('PC_END',index,stem,result$status,'diagnostic_elapsed',result$diagnostic_elapsed,result$error,'\n');flush.console()
}
cat('DONE total diagnostic_elapsed',proc.time()[['elapsed']]-batch,'\n')

