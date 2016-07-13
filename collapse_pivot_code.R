#there were 5 steps to clean the DSM data
# Steps 3-5 were done in Python and Excel rest were done in R

################################# STEP 1: LOADING AND EXPANDING THE DATA  ##########################
#install.packages("dplyr")
library(dplyr)

#read your file :dsm <- read.csv("~/your path to file ") 
#file name is "dsm"
dsm1 <- select(dsm, Codes, Chapter, Category, Symptom) #make sure the column names are consistent
#make dataframe of everything needed
dsmf <- as.data.frame(dsm1)
dsmf[sapply(dsmf, is.factor)] <- lapply(dsmf[sapply(dsmf, is.factor)],as.character)
str(dsmf)

#give each category its own row 
splitCat <- strsplit(dsmf$Category, split = ",")
repCatDsm <- data.frame(Codes = rep(dsmf$Codes, sapply(splitCat, length)), Chapter = rep(dsmf$Chapter, sapply(splitCat, length)), Symptoms = rep(dsmf$Symptoms, sapply(splitCat, length)), Category = unlist(splitCat))
head(repCatDsm)

#give each code their own row
splitCodes <- strsplit(dsmf$Codes, split = ",")
ndsm<- data.frame(Category = rep(dsmf$Category, sapply(splitCodes, length)),Chapter=rep(dsmf$Chapter, sapply(splitCodes, length)),  Symptoms = rep(dsmf$Symptoms, sapply(splitCodes, length)), Codes = unlist(splitCodes))
summary(ndsm)
head(ndsm)

##############################  STEP 2: COLLAPSE ACCORDING TO CODES #################################

#collapse  Categories according to codes
dsmCat<- aggregate(ndsm$Category, list(ndsm$Codes), paste, collapse=" , ")
names(dsmCat)[names(dsmCat)=="Group.1"] <- "Codes"
names(dsmCat)[names(dsmCat)=="x"] <- "Categories"

#collapse  Chapter according to codes
dsmChap<- aggregate(ndsm$Chapter, list(ndsm$Codes), paste, collapse = ',')
names(dsmChap)[names(dsmChap)=="Group.1"] <- "Codes"
names(dsmChap)[names(dsmChap)=="x"] <- "Chapter"

#collapse Symptoms according to code
dsmSymp<- aggregate(ndsm$Symptoms, list(ndsm$Codes), paste, collapse ='.')
names(dsmSymp)[names(dsmSymp)=="Group.1"] <- "Codes"
names(dsmSymp)[names(dsmSymp) == "z"] <- "Symptoms"

#Merge the three
dsm2 <- merge(dsmCat, dsmChap, by = "Codes")
dsm3 <- merge( dsm2, dsmSymp , by = "Codes")


#export the collapsed file
write.csv(dsm3, "160616 Collapsed.csv" )
###########################          STEP 3 - 5        ########################################################


# STEP 3: Take the file from STEP 2 and Clean redundant Chapters and duplicates in Python
# STEP 4: Export out all the Codes with and without Ors into a seprate file 
# STEP 5: Manually duplicate the Ors so their symptoms are all reflected (more instructions) and append them to the master data file


###########################  STEP 5: MAKE DUMMY VARIABLES ########################################################

#read your file :dsm4 <- read.csv("~/your path to file ") 
#file name of all the cleaned "dsm4"

#Categories in our file
catfordsm <- list(c("adl" , "apathy" , "attachment", "attention" , "avoidance","behavior","cogdev", "communication" , "delusion" , "detachment", "duration", "eating","feeling","hallucination", "iho", "impulse", "memory", "mood","motor", "onset", "orientation","prereq","rigidity","risk","ritual", "self-concept" , "self-harm" , "sensory","sexual","sleep",  "somatic", "substance", "thought"
))

pivot.f<- mutate(dsm4 , 
            adl = grepl("adl",Categories), 
            apathy= grepl("apathy",Categories), 
            attachment=  grepl("attachment", dsm4$Categories),
            attention= grepl("attention",dsm4$Categories),
            avoidance = grepl("avoidance",dsm4$Categories), 
            behavior= grepl("behavior",dsm4$Categories), 
            cogdev= grepl("cogdev",dsm4$Categories), 
            communication= grepl("communication",dsm4$Categories), 
            eating= grepl("eating",dsm4$Categories) ,
            judgement= grepl("judgement",dsm4$Categories), 
            memory= grepl("memory",dsm4$Categories), 
            prereq= grepl("prereq",dsm4$Categories),
            concentration= grepl("concentration",dsm4$Categories),
            delusion= grepl("delusion",dsm4$Categories),
            detachment= grepl("detachment",dsm4$Categories),
            duration= grepl("duration",dsm4$Categories),
            feeling= grepl("feeling",dsm4$Categories),
            hallucination= grepl("hallucination",dsm4$Categories),
            hallucination= grepl("hallucinations",dsm4$Categories),
            iho= grepl("iho",dsm4$Categories),
            impulse= grepl("impulse",dsm4$Categories),
            mood=grepl("mood",dsm4$Categories),
            motor=grepl("motor",dsm4$Categories),
            onset=grepl("onset",dsm4$Categories),
            orientation=grepl("orientation",dsm4$Categories),
            prereq=grepl("prereq",dsm4$Categories),
            rigidity=grepl("rigidity",dsm4$Categories),
            risk=grepl("risk",dsm4$Categories),
            ritual=grepl("ritual",dsm4$Categories),
            self.concept=grepl("self-concept",dsm4$Categories),
            self.harm=grepl("self-harm",dsm4$Categories),
            sensory=grepl("sensory",dsm4$Categories),
            sleep=grepl("sleep",dsm4$Categories),
            sexual=grepl("sexual",dsm4$Categories),
            somatic=grepl("somatic",dsm4$Categories),
            substance=grepl("substance",dsm4$Categories),
            thought=grepl("thought",dsm4$Categories)
)


#convert to Binary
pivot.f [pivot.f == "TRUE"] <- "1"
pivot.f [pivot.f == "FALSE"] <- "0"
pdsm <- pivot.f
#take out the catrgories and symptoms if needed
pdsm$Categories<-NULL
pdsm$Symptoms<-NULL

#export the pivoted file 
write.csv(pdsm, "pivoted_DSM_data.csv" )





