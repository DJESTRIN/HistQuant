library(ggplot2)
library(readxl)
library(nlme)
library(emmeans)

SegmentDendrites <- read_excel("C:/Users/David/Downloads/dendritic_segments_output/Segment - Dendrites.xlsx")
st.err<-function(x){sd(x)/sqrt(length(x))}
SegmentDendrites$group<-as.factor(SegmentDendrites$group)
SegmentDendrites$layer<-as.factor(SegmentDendrites$layer)
levels(SegmentDendrites$group)[levels(SegmentDendrites$group)=='GROUPCHR2'] <- 'ChR2'
levels(SegmentDendrites$group)[levels(SegmentDendrites$group)=='GROUPGFP'] <- 'GFP'

levels(SegmentDendrites$layer)[levels(SegmentDendrites$layer)=='LAYER1'] <- 'Layer 1'
levels(SegmentDendrites$layer)[levels(SegmentDendrites$layer)=='LAYER23'] <- 'Layers 2 & 3'
levels(SegmentDendrites$layer)[levels(SegmentDendrites$layer)=='LAYER45'] <- 'Layers 4 & 5'


density<-aggregate(Density~group+animal+neuronid+layer,data=SegmentDendrites, FUN="mean")
density_av<-aggregate(Density~group,data=density, FUN="mean")
density_averr<-aggregate(Density~group,data=density, FUN=st.err)
density_av$error<-density_averr$Density

p<-ggplot(data=density, aes(x=group,y=Density,color=group,fill=group))+
  geom_jitter(width=0.05,alpha=0.3, aes(group=neuronid),size=2)+
  geom_errorbar(data=density_av,aes(x=group,ymin=Density-error, ymax=Density+error,color=group),width=0,size=1.5)+
  geom_point(data=density_av,aes(x=group,y=Density,fill=group,color=group),size=10)+
  geom_point(data=density_av,aes(x=group,y=Density,fill=group,color="white"),size=7)+
  theme_bw() +
  ylab("Dendritic Spine Density (spines/um)") + xlab("") +
  theme(axis.line = element_line(colour = "black", size=1.1),
        axis.ticks = element_line(colour = "black", size = 2),
        axis.text=element_text(size=12,colour = "black", face = "bold"),
        axis.title=element_text(size=14,colour = "black",face="bold"),
        strip.background = element_rect(color="white", fill="white", size=1.5, linetype="solid"),
        strip.text = element_text(size = 14, face = "bold.italic"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        legend.position = "none")+
  scale_fill_manual(values=c("#E69F00", "#56B4E9", "white"))+
  scale_color_manual(values=c("#E69F00", "#56B4E9", "white"))
print(p)

m1 <- lme(Density~group, random=~1|animal, data=density)
anova(m1)
estimates<-emmeans(m1, ~group)
pairs(estimates, adjust="fdr")



density<-aggregate(Density~group+animal+neuronid+layer,data=SegmentDendrites, FUN="mean")
density_av<-aggregate(Density~group+layer,data=density, FUN="mean")
density_averr<-aggregate(Density~group+layer,data=density, FUN=st.err)
density_av$error<-density_averr$Density

p<-ggplot(data=density, aes(x=group,y=Density,color=group,fill=group))+
  geom_jitter(width=0.05,alpha=0.3, aes(group=neuronid))+
  geom_errorbar(data=density_av,aes(x=group,ymin=Density-error, ymax=Density+error,color=group),width=0,size=2)+
  geom_point(data=density_av,aes(x=group,y=Density,fill=group,color=group),size=10)+
  geom_point(data=density_av,aes(x=group,y=Density,fill=group,color="white"),size=7)+
  facet_wrap(.~layer)+
  theme_bw() +
  ylab("Dendritic Spine Density (spines/um)") + xlab("") +
  theme(axis.line = element_line(colour = "black", size=1.1),
        axis.ticks = element_line(colour = "black", size = 2),
        axis.text=element_text(size=12,colour = "black", face = "bold"),
        axis.title=element_text(size=14,colour = "black",face="bold"),
        strip.background = element_rect(color="white", fill="white", size=1.5, linetype="solid"),
        strip.text = element_text(size = 14, face = "bold.italic"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        legend.position = "none")+
  scale_fill_manual(values=c("#E69F00", "#56B4E9", "white"))+
  scale_color_manual(values=c("#E69F00", "#56B4E9", "white"))
print(p)

m2 <- lme(Density~group*layer, random=~1|animal, data=density)
anova(m2)
emmip(m2, group ~ layer)
estimates<-emmeans(m2, ~group*layer)
print(estimates)
pairs(estimates, adjust="fdr")

length<-aggregate(length~group+animal+neuronid+layer,data=SegmentDendrites, FUN="mean")
length_av<-aggregate(length~group,data=length, FUN="mean")
length_averr<-aggregate(length~group,data=length, FUN=st.err)
length_av$error<-length_averr$length

p<-ggplot(data=length, aes(x=group,y=length,color=group,fill=group))+
  geom_jitter(width=0.05,alpha=0.3, aes(group=neuronid))+
  geom_errorbar(data=length_av,aes(x=group,ymin=length-error, ymax=length+error,color=group),width=0,size=1)+
  geom_point(data=length_av,aes(x=group,y=length,fill=group,color=group),size=2)
print(p)

m3 <- lme(length~group*layer, random=~1|animal, data=length)
anova(m3)
emmip(m3, group ~ layer)
estimates<-emmeans(m3, ~group*layer)
print(estimates)
pairs(estimates, adjust="fdr")

volume<-aggregate(volume~group+animal+neuronid+layer,data=SegmentDendrites, FUN="mean")
volume_av<-aggregate(volume~group,data=volume, FUN="mean")
volume_averr<-aggregate(volume~group,data=volume, FUN=st.err)
volume_av$error<-volume_averr$volume

p<-ggplot(data=volume, aes(x=group,y=volume,color=group,fill=group))+
  geom_jitter(width=0.05,alpha=0.3, aes(group=neuronid))+
  geom_errorbar(data=volume_av,aes(x=group,ymin=volume-error, ymax=volume+error,color=group),width=0,size=1)+
  geom_point(data=volume_av,aes(x=group,y=volume,fill=group,color=group),size=2)
print(p)

m4 <- lme(volume~group*layer, random=~1|animal, data=volume)
anova(m4)
emmip(m4, group ~ layer)
estimates<-emmeans(m4, ~group*layer)
print(estimates)
pairs(estimates, adjust="fdr")
