# This work is based on: https://rstudio-pubs-static.s3.amazonaws.com/31867_8236987cf0a8444e962ccd2aec46d9c3.html

Needed <- c("tm", "SnowballCC", "RColorBrewer", "ggplot2", "wordcloud", "biclust", "cluster", "igraph", "fpc")
install.packages(Needed, dependencies=TRUE)
install.packages("Rcampdf", repos = "http://datacube.wu.ac.at/", type = "source")

# Load text files on mac
cname <- file.path("~", "Desktop", "20160718-150239-berlin")

# Load text files on windows
#cname <- file.path("C:", "20160718-150239-berlin")

# List file names of loaded files
dir(cname)

# Load the "Text Mining" library
library(tm)

# Load "Snowball stemmers based on the C libstemmer UTF-8" library
library(SnowballC)

# Load "Grammar of Graphics" library
library(ggplot2)

# Load "Wordcloud" library
library(wordcloud)

# Create a corpus out of the texts
docs <- Corpus(DirSource(cname))

# Remove punctuation
docs <- tm_map(docs, removePunctuation)

# Remove numbers
docs <- tm_map(docs, removeNumbers)

# Convert everything to lowercase
docs <- tm_map(docs, tolower)

# Remove stopwords
docs <- tm_map(docs, removeWords, stopwords("english"))

# Remove custom words
docs <- tm_map(docs, removeWords, c("berlin", "hotel", "room", "rooms", "stayed"))

# Apply stemming
docs <- tm_map(docs, stemDocument)

# Remove whitespace
docs <- tm_map(docs, stripWhitespace)

# Treat preprocessed documents as text documents
docs <- tm_map(docs, PlainTextDocument)

# Create document term matrix
dtm <- DocumentTermMatrix(docs)
dtm

# Remove sparse terms
dtms <- removeSparseTerms(dtm, 0.99) # This makes a matrix that is 99% empty space, maximum.
dtms

# Organise terms by frequency
freq <- sort(colSums(as.matrix(dtms)), decreasing=TRUE)
freq

# View of term frequency
wf <- data.frame(word=names(freq), freq=freq)
head(wf)

# Plot words that appear at least x times
p <- ggplot(subset(wf, freq>10000), aes(word, freq))
p <- p + geom_bar(stat="identity")
p <- p + theme(axis.text.x=element_text(angle=45, hjust=1))
p
ppi <- 300
dev.copy(png, "plot_minfreq10000_berlin.png", width=6*ppi, height=6*ppi, res=ppi)
dev.off()

# Plot words that occur at least x times
set.seed(142)
wordcloud(names(freq), freq, min.freq=1000, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"))
ppi <- 300
dev.copy(png, "word_cloud_minfreq2000_berlin.png", width=6*ppi, height=6*ppi, res=ppi)
dev.off()

# Plot the x most frequently used words
set.seed(142)
wordcloud(names(freq), freq, max.words=1000, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"))
ppi <- 300
dev.copy(png, "word_cloud_mostfreq1000_berlin.png", width=6*ppi, height=6*ppi, res=ppi)
dev.off()
