library(ggplot2)  

plotPhylum <- function(df){
    phylum <- df[df$rank == 'phylum' & phylum$percent_abundance >= 0.3, ] 
    ggplot(phylum , aes(x=sample, y=percent_abundance, fill=taxon)) +
        geom_bar(stat="identity") +  
        xlab('Sample') + 
        ylab('Abundance') +
        labs(fill='Phylum') +
        theme(axis.text.x = element_text(angle = 90))
}

plotFamily <- function(df){
    family <- df[df$rank == 'family' & family$percent_abundance >= 0.3, ] 
    ggplot(family , aes(x=sample, y=percent_abundance, fill=taxon)) +
        geom_bar(stat="identity") +  
        xlab('Sample') + 
        ylab('Abundance') +
        labs(fill='Family') +
        theme(axis.text.x = element_text(angle = 90)) 
}
