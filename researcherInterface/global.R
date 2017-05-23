library(shiny)
library(ggplot2)
library(rpart)
library(readr)
library(randomForest)
library(tidyverse)
library(party)
library(plotly)
suppressPackageStartupMessages(library(heatmaply))
library(heatmaply)
library(rpart.plot)

#pivot <- read_csv("~/Google Drive/2017classes/Mental health : Model and Visual/mental-health-project/Mental Health Interface/pivot.csv")

symptoms<- c("adl", "attachment", "attention","avoidance", 
             "behavior" ,"cogdev" ,"communication","concentration",
             "delusion","detachment","duration","feeling",
             "hallucination","iho" ,"impulse","motor","onset",
             "orientation","prereq","rigidity","risk","self.concept" ,
             "self.harm","sensory","sleep","sexual","somatic" ,
             "substance","thought" )


pivotMod <- select(pivot, -Code, -Symptom, -X1)
pivotMod$Chapter <- as.factor(pivotMod$Chapter)

#Fit tree
rpart.tree <- rpart(Chapter ~ ., data=pivotMod)


#Chap similarity
#chapFreq <- read_csv("~/Google Drive/2017classes/Mental health : Model and Visual/mental-health-project/Mental Health Interface/outputfile.csv")
#chapFreq<- read_csv("outputfile.csv")
#chaps<- 1:19
#Chapter<- as.array(chaps)
#Frequency <- as.array(c("28","13","1","0","6","6","7","2","14","0","2","14","7","2","3","30","2","1","2"))
#chapFreq <- data.frame(Chapter,Frequency)
#chapFreq$Chapter <- as.factor(chapFreq$Chapter)
#chapFreq_plot <- ggplot(chapFreq, aes(x = Chapter, y = Frequency, text = paste("Chapter:", Chapter, "<br>", "Number of Non-distinguishable Diagnoses:", Frequency))) + geom_bar(stat = "identity", fill = I("skyblue")) + 
 # theme_classic() + ylab("Number of Non-distinguishable Diagnoses per Chapter")
#chap_freq<- ggplotly(chapFreq_plot, tooltip = c("text"))

#Random Forest var imp
set.seed(1)
rf <- randomForest(Chapter~., data = pivotMod, importance = TRUE)
mean_dec_acc <- as.data.frame(importance(rf, type = 1))
mean_dec_acc <- add_rownames(mean_dec_acc, "Symptom")
mean_dec_acc <- arrange(mean_dec_acc, desc(MeanDecreaseAccuracy))

#random Forest
varchap <- select(var.imp, -MeanDecreaseAccuracy,-MeanDecreaseGini)



# error rate 
misclass <- as.data.frame(rf$confusion)
misclass <- add_rownames(misclass, "Chapter")
misclass<- mutate(misclass, Occurance = rowSums(misclass[2:20])) 
misclass$Chapter <- factor(misclass$Chapter, levels = c("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"))



########################### Chapters ##########################
Chapter.Number<- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
Chapter.Title <- c("Neurodevelopmental Disorders", "Schizophrenia Spectrum and Other Psychotic Disorders", "
Bipolar and Related Disorders", "Depressive Disorders", "Anxiety Disorders", "Obsessive-Compulsive and Related Disorders", "Trauma- and Stressor-Related Disorders", "Dissociative Disorders", "Somatic Symptom and Related Disorders", "Feeding and Eating Disorders", "Elimination Disorders", "Sleep-Wake Disorders", "Sexual Dysfunctions", "Gender Dysphoria", "Disruptive, Impulse-Control, and Conduct Disorders", "Substance-Related and Addictive Disorders", "Neurocognitive Disorders", "Personality Disorders", "Paraphilic Disorders")
dsm5 <- data.frame(Chapter.Number,Chapter.Title)




des1<-("The Diagnostic and Statistical Manual of Mental Disorders (5th ed.; DSM–5; American Psychiatric Association, 2013) classifies mental health conditions and the criteria necessary to make each diagnosis. 
As such, it is a tool used by mental health clinicians to aid them in making diagnoses and determining treatments. The DSM-5 is organized into 20 chapters, each of which lists possible diagnoses of a particular type, 
such as neurodevelopmental disorders, depressive disorders, and anxiety disorders. (Click the Chapter Key to see what each of the chapters are)")

des2<- ("There exists a disconnect between the tightly-controlled laboratory studies being referenced and the application of visualization tools in practice. The Computing for Mental Health project 
        at the Smith College Human Computation and Visualization Laboratory (HCV) has been working on a way to bridge this disconnect. The goal of the Mental Health Project is to build an interactive tool to reduce a clinician’s specialization bias while making mental health diagnoses. 
        There are two interfaces of the tool : a Clinician Interface and a Researcher Interface. This is the researcher Interface and it uses machine learning techniques like clustering, decision tree and random forests to help researcher 
        understand the structure of the DSM-5 and classify Chapters in the DSM based on Symptoms. ")

des3<- ("Once a clinician decides to look for a particular diagnosis or even a particular chapter, the clinician is essentially bound to a diagnosis in that chapter. However, sometimes a diagnosis in a different chapter 
        might be more appropriate. For instance, if a clinician’s patient had difficulty sleeping, the clinician might turn to the “Sleep-Wake Disorders” section of the DSM-5 and assign a diagnosis from that chapter. 
        Yet “persistent reluctance or refusal to sleep away from home or to go to sleep without being near a major attachment figure” is also a symptom of separation anxiety disorder, which is in the “Anxiety Disorders” chapter. 
        But because the clinician did not reference the “Anxiety Disorders” chapter, the clinician would not have been presented with all possible disorders - and thus might make a nonoptimal diagnosis.Our system helps 
        mental health clinicians more accurately diagnose mental health conditions without specialization bias")

des4 <-("There are three key parts to this  interface :")
des5 <-("Lets the researcher filter and select the data they want to see")
des6 <-("A researcher can tune, prune and view the results of the decision tree model from the Rpart and Party package")
des7 <-("Shows results of a Random Forest and our own Chapter Similarity algorithmn to show which symptoms or chapter may get
missclassified")