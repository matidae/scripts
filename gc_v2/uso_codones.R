#Uso de codones por gen

plot_data<-function(filename, percentage, title){
    data = read.csv(file = filename, sep = "\t", header = FALSE)
    data_order <- data[order(data[,2]),]
    number_of_genes = as.integer(nrow(data_order) * percentage / 100)
    low_exp = data_order[1:number_of_genes,]
    high_exp = data_order[(nrow(data_order) - number_of_genes + 1 ):nrow(data_order),]

    print("## High exp.##")
    print (paste("n =",nrow(high_exp), "/",nrow(data) , percentage, "%" ,"; mean gc =", mean(high_exp[3]), "; mean exp =", mean(high_exp[,2])))
    print("## Low exp.##")
    print (paste("n =",nrow(low_exp), "/",nrow(data) , percentage, "%" ,"; mean gc =", mean(low_exp[3]), "; mean exp =", mean(low_exp[,2])))

    high_exp_hist <- hist(high_exp[,3], breaks = 70, plot = FALSE)
    low_exp_hist <- hist(low_exp[,3], breaks = 70, plot = FALSE)

    max_graph = max(high_exp_hist$count, low_exp_hist$count)

    plot(
         low_exp_hist, 
         xaxt = "n", yaxt = "n", 
         xlim = c(0.1,1), ylim = c(0,max_graph + max_graph/10),
         col = rgb(0,0,1,0.3),
         xlab = "GC3 content", ylab = "Number of genes",
         main = paste(title, " GC3 content"),
         freq = TRUE
    )
    
    axis(1, at = seq(0, 1, by = 0.05), lwd = 1, lwd.ticks = 1)
    axis(2, at = seq(0, max_graph + max_graph/10, 10))

    plot(
         high_exp_hist,
         xaxt = "n" , yaxt = "n", 
         col = rgb(0, 1, 0, 0.2),
         add = TRUE, freq = TRUE,
        )
    legend("topleft", c("Higher expression","Lower expression"), fill = rgb(0, 1:0, 0:1, 0.4), bty = "n")

}

