
# General

## ACM: Engineering Research (AKA Design Science)
Research that invents and evaluates technological artifacts. 

### Application
This standard applies to manuscripts that propose and evaluate technological artifacts, including algorithms, models, languages, methods, systems, tools, and other computer-based technologies. 

This standard is not appropriate for: 
     - evaluations of pre-existing engineering research approaches (consider the **Experiments Standard**)
     - experience reports of applying pre-existing engineering research approaches.

## ACM: Multi-Methodology and Mixed Methods Research
Studies that use two or more approaches to data collection or analysis to corroborate, complement and expand research findings (multi-methodology) or combine and integrate inductive research with deductive research (mixed methods), often but not necessarily relying on qualitative and/or quantitative data.

### Application

This standard applies to software engineering studies that use two or more data collection or analysis methods. It enumerates criteria related to the mixing of methodologies, not the methodologies themselves. For the latter, refer to **method-specific standards**. For example, a multi-methodology study combining a case study with an experiment should comply with **The Case Study Standard** and **The Experiment Standard** as well as this standard.

# Qualitative

## ACM: Action Research
Empirical research that investigates how an intervention, like the introduction of a method or tool, affects a real-life context
### Application

This standard applies to empirical research that meets the following conditions.

-    investigates a primarily social phenomenon within its real-life, organizational context
-    intervenes in the real-life context (otherwise, see the **Case Study Standard**)
-    the change and its observation are an integral part of addressing the research question and contribute to research

If the intervention primarily alters social phenomena (e.g. the organization’s processes, culture, way of working or group dynamics), use this standard. If the intervention is a new technology or technique (e.g. a testing tool, a coding standard, a modeling grammar), especially if it lacks a social dimension, consider the **Engineering Research Standard**. If the research involves creating a technology and an organizational intervention with a social dimension, consider both standards.

## ACM: Case Study and Ethnography
"An empirical inquiry that investigates a contemporary phenomenon (the "case") in depth and within its real-world context, especially when the boundaries between phenomenon and context are unclear" (Yin 2017)

### Application

This standard applies to empirical research that meets the following conditions.

-    Presents a detailed account of a specific instance of a phenomenon at a site. The phenomenon can be virtually anything of interest (e.g. Unix, cohesion metrics, communication issues). The site can be a community, an organization, a team, a person, a process, an internet platform, etc.
-    Features direct or indirect observation (e.g. interviews, focus groups)—see Lethbridge et al.’s (2005) taxonomy.
-    Is not an experience report (cf. Perry et al. 2004) or a series of shallow inquiries at many different sites.

A case study can be brief (e.g. a week of observation) or longitudinal (if observation exceeds the natural rhythm of the site; e.g., observing a product over many releases). For our purposes, case study subsumes ethnography.

If data collection and analysis are interleaved, consider the **Grounded Theory Standard**. If the study mentions action research, or intervenes in the context, consider the **Action Research Standard**. If the study captures a large quantitative dataset with limited context, consider the **Data Science Standard**.

## ACM: Grounded Theory
A study of a specific area of interest or phenomenon that involves iterative and interleaved rounds of qualitative data collection and analysis, leading to key patterns (e.g. concepts, categories)
### Application

This standard applies to empirical inquiries that meet all of the following conditions:

-    Explores a broad area of investigation without specific, up-front research questions.
-    Applies theoretical sampling with iterative and interleaved rounds of data collection and analysis.
-    Reports rich and nuanced findings, typically including verbatim quotes and samples of raw data.

For predominately qualitative inquiries that do not iterate between data collection and analysis or do not use theoretical sampling, consider the **Case Study Standard** or the **Qualitative Survey Standard**.

## ACM: Qualitative Surveys (Interview Studies)
Research comprising semi-structured or open-ended interviews

### Application

This standard applies to empirical inquiries that meet all of the following criteria:

-    Researcher(s) have synchronous conversations with one participant at a time
-    Researchers ask, and participants answer, open-ended questions
-    Participants’ answers are recorded in some way
-    Researchers apply some kind of qualitative data analysis to participants’ answers

If researchers iterated between data collection and analysis, consider the **Grounded Theory Standard**. If respondents are all from the same organization, consider the **Case Study Standard**. If researchers collect written text or conversations (e.g. StackExchange threads), consider the **Discourse Analysis Standard** (not yet available).

# Quantitative

## ACM: Benchmarking (of Software Systems)
A study in which a software system is assessed using a standard tool (i.e. a benchmark) for competitively evaluating and comparing methods, techniques or systems "according to specific characteristics such as performance, dependability, or security” (Kistowski et al. 2015).

### Application

This standard applies to empirical research that meets the following conditions.

-    investigates software systems within a defined context with an automated, repeatable procedure
-    studies the software system’s quality of service under a specific workload or usage profile

If the benchmark experiments primarily study software systems, use this standard. For experiments with human participants, see the **Experiments (with Human Participants) Standard**. For simulation of models of the software systems, see the **Simulation (Quantitative) Standard**. If the study is conducted within a real-world context, see the **Case Study and Ethnography Standard**. Benchmarking is often used with Engineering Research (see the **Engineering Research (AKA Design Science) Standard**).

## ACM: Data Science
Studies that analyze software engineering phenomena or artifacts using data-centric analysis methods such as machine learning or other computational intelligence approaches as well as search-based approaches [Dhar, V. (2013). Data Science and Prediciton, Communications of the ACM, December 2013, Vol. 56 No. 12, Pages 64-73. https://cacm.acm.org/magazines/2013/12/169933-data-science-and-prediction/fulltext].


### Application

Applies to studies that primarily analyze existing software phenomena using predictive, preemptive or corrective modelling.

-    If the analysis focuses on the toolkit, rather that some new conclusions generated by the toolkit, consider the **Artifacts Standard**
-    If the analysis focuses on a single, context-rich setting (e.g., a detailed analysis of a single repository), consider the **Case Study Standard**.
-    If the temporal dimension is analyzed, consider the **Longitudinal Studies Standard**.
-    If the data objects are discussions or messages between humans, consider the **Discourse Analysis Standard**.
-    If data visualizations are used, consider the Information Visualization Supplement. (With large data sets especially, care is needed to keep visualizations legible.)
-    If the analysis selects a subset of available data, consult the Sampling Supplement.

## ACM: Experiments (with Human Participants)
A study in which an intervention is deliberately introduced to observe its effects on some aspects of reality under controlled conditions
### Application

This standard applies to controlled experiments and quasi-experiments that meet all of the following conditions:

-    manipulates one or more independent variables
-    controls many extraneous variables
-    applies each treatment independently to several experimental units
-    involves human participants

In true experiments, experimental units are randomly allocated across treatments; quasi-experiments lack random assignment. Experiments include between-subjects, within-subjects and repeated measures designs. For experiments without human participants, see the **Exploratory Data Science Standard** or the **Engineering Research Standard**.

## ACM: Longitudinal Studies
A study focusing on the changes in and evolution of a phenomenon over time

### Application

This standard applies to studies that involve repeated observations of the same variables (e.g., productivity or technical debt) over a period of time. Longitudinal studies include the analysis of datasets over time, such as the analysis of the evolution of the code. Longitudinal studies require to maintain identifiability of subjects (humans or artifacts) between data collection waves and to use at least two waves.

For cross-sectional analysis, consider the **Exploratory Data Science Standard** or the **Experiments Standard** (if variables are manipulated).

## ACM: Optimization Studies in SE (including Search-Based Software Engineering)
Research studies that focus on the formulation of software engineering problems as search problems, and apply optimization techniques to solve such problems1.
### Application

This standard applies to empirical studies that meet the following criteria:

-    Formulates a software engineering task as an optimization problem, with one or more specified fitness functions3 used to judge success in this task.
-    Applies one or more approaches that generate solutions to the problem in an attempt to maximize or minimize the specified fitness functions.

## ACM: Simulation (Quantitative)
A study that involves developing and using a mathematical model that imitates a real-world system's behavior, which often entails problem understanding, data collection, model development, verification, validation, design of experiments, data analysis, and implementation of results.

### Application

The standard applies to research studies that use simulation to understand, assess or improve a system or process and its behavior. Use this standard for in silico simulations, i.e., studies representing everything using computational models. For in virtuo simulations, i.e., human participants manipulating simulation models, use the **Experiments (with human participants) Standard**. For simulations used to assess a new or improved technological artifact, also consider the **Engineering Research standard**.

## ACM: Questionnaire Surveys
A study in which a sample of respondents answer a series of (mostly structured) questions, typically through a computerized or paper form

### Application

This guideline applies to studies in which:

-    a sample of participants answer predefined, mostly closed-ended questions (typically online or on paper)
-    researchers systematically analyze participants’ answers

This standard does not apply to questionnaires comprising predominately open-ended questions[1], literature surveys (see the Systematic Review Standard), longitudinal or repeated measures studies (see the **Longitudinal Studies Standard**), or the demographic questionnaires typically given to participants in controlled experiments (see the **Experiments Standard**).

[1] There is currently no standard for predominately open-ended questionnaire surveys. One exemplar readers could draw from is: Daniel Graziotin, Fabian Fagerholm, Xiaofeng Wang, and Pekka Abrahamsson. 2018. “What happens when software developers are (un)happy.” Journal of Systems and Software 140, 32-47.

## ACM: Repository Mining
A study that quantitatively analyzes a dataset extracted from a platform hosting of structured or semi-structured text (e.g a source code repository)
### Application

The standard applies to software engineering studies that: - use automated techniques to extract data from large-scale data repositories such as source code repositories, mailing list archives, bug tracking systems, Q&A forums and chat communication platforms - quantitatively analyze the contents mined from the repositories

If the study focuses on predictive modeling (e.g. machine learning) consider the **Data Science Standard**. If the subject systems are a few context-rich repositories, consider the **Case Study Standard**. If the analysis is predominately qualitative, refer to methodological guidelines for qualitative content analysis or discourse analysis (standard TBD).

# Literature Review

## ACM: Case Survey (AKA Case Meta-Analysis)
A study that aims to generalize results about a complex phenomenon by systematically converting qualitative descriptions available in published case studies into quantitative data and analyzing the converted data

### Application

This standard applies to studies in which:

-    a sample of previously published case studies is obtained;
-    the qualitative case descriptions are converted systematically into quantitative data; and
-    the converted quantitative data is analyzed to reach generalizable results.

This standard does not apply to studies collecting primary data from a large number of instances of a phenomenon; for instance, using interviews (consider the **Qualitative Survey Standard**) or questionnaires (consider the **Questionnaire Survey Standard**). For individual case studies use the **Case Study Standard**. For reviews of other kinds of studies (e.g., experiments) consider the **Systematic Review Standard**. This standard also does not apply to qualitative synthesis (e.g. meta-ethnography, narrative synthesis).

## ACM: Systematic Reviews
A study that appraises, analyses, and synthesizes primary or secondary literature to provide a complete, exhaustive summary of current evidence regarding one or more specific topics or research questions

### Application

-    Applies to studies that systematically find and analyze existing literature about a specified topic
-    Applies both to secondary and tertiary studies
-    Does not apply to ad-hoc literature reviews, case surveys or advanced qualitative synthesis methods (e.g. meta-ethnography)

# Other

## ACM: Methodological Guidelines and Meta-Science
A paper that analyses an issue of research methodology or makes recommendations for conducting research.

### Application

This standard applies to papers that provide analysis of one or more methodological issues, or advice concerning some aspect of research.

-    may or may not include primary or secondary empirical data or analysis.
-    may consider philosophical or practical issues
-    may simultaneously be a methodology paper and an empirical study, to which another standard also applies; for example, if a paper reports a case study and then gives advice about a methodological issue illuminated by the case study, consider both **this standard** and the **Case Study Standard**.

## ACM: Replication
A study that deliberately repeats a previous study (the "original study") to determine whether its results can be reproduced (Carver et al., 2013)

### Application

This standard applies to empirical studies that meet the following criteria:

-    The replication attempt is deliberate and planned, not accidental overlap with a previous study.
-    The original study is clearly identified as a separate previous publication. If the replication is not the only replication of the original study, i.e., it is a part of a family of replications, all the other replications are identified and the current replication is clearly defined in the context of the family.
