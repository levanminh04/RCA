# Determinism and reversed input-column probe on the two predeclared cases.
source('D:/RCA-ext/work/T-014/CIRCA/circa/graph/r/causal.R')
root <- 'D:/RCA-ext/work/T-014/audit-r/'
records <- list()
for (stem in c('cartservice_cpu_1','cartservice_mem_1')) {
  d <- read.csv(paste0(root,stem,'_input.csv'),check.names=FALSE)
  first <- as.matrix(read.csv(paste0(root,stem,'_pcalg.csv'),check.names=FALSE))
  again <- runPC(as.matrix(d),CItest='gauss',alpha=.05,m.max=Inf,numCores=1)
  perm <- rev(seq_len(ncol(d)))
  reordered <- runPC(as.matrix(d[,perm]),CItest='gauss',alpha=.05,m.max=Inf,numCores=1)
  mapped <- reordered[order(perm),order(perm)]
  write.csv(mapped,paste0(root,stem,'_pcalg_reordered_mapped.csv'),row.names=FALSE)
  record <- data.frame(stem=stem,repeat_same=all(first==again),repeat_num_edge_differences=sum(first!=again),
                       permutation_same=all(first==mapped),permutation_num_edge_differences=sum(first!=mapped))
  records[[length(records)+1]] <- record
  print(record)
}
write.csv(do.call(rbind,records),'D:/RCA-flashticket/results/T-014/audit/pcalg-repeat.csv',row.names=FALSE)
