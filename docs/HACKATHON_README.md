# SEC_StagHack2025

## The Schedule
- 9:00 - 9:30 welcome and explanation of the rules
- 9:30 - noon code away!
- noon - 1:00 - lunch and presentation by Nick Mercadante
- 1:00 - 2:00 - code away! (LAST COMMIT AT 2:00 PM!)
- 2:00 - 2:30 - judges will meet for the final ranking
- 2:30 - 2:45 - award ceremony!

## First a little bit of context
Scheduling is a common problem in healthcare practices. At [PursueCare](https://www.pursuecare.com/), our patients deal with a variety of mental health and substance abuse issues. Given the nature of these issues, it can be difficult to get patients to continue treatment after a certain point. Looking back at our own data we can see that **the earlier we can get a new patient into their first appointment they have a higher chance of staying with treatment** to a statistically significant degree. The current new patient scheduling process is manual. Your goal is to design an algorithm using anonymized patient data that minimizes the time to the first appointment.

## Project Goal: 
- Build an algorithm (or more than one) that minimizes the time between the registration of a patient to a portal and the time of the first appointment with a healthcare provider.

## Dev tools:
You can use any programming/scripting language. 

## The Data
To solve this problem we are going to provide some data, which is organized in 4 tables. Each table outlined below has a brief description and documentation on each field that is going to be used. **_New Patient Data_** contains patients who have not had their first appointment scheduled and the program they are enrolled in (Mental Health/SUD). **_Appointment Data_** contains existing appointments for the month of January ’25. The existing appointments in this dataset cannot be booked over and need to be scheduled around, the only exception is ‘cancelled’ appointments which can be removed during data preprocessing. **_Provider Schedule Data_** contains one week worth of provider availability that should be repeated for each week in January ’25. **_Provider State Data_** contains information on what providers are licensed in certain states. Your algorithm needs to ensure that each new patient is scheduled with a provider that is eligible to practice medicine in that state. 

### New Patient Data: Patients that need their first appointment scheduled
-	PATIENTID: unique key that represents an individual patient
-	STATE: State code for patients residence
-	REGISTRATIONDATE: Date where patient is introduced to PursueCare but has not yet received care
-	PROGRAM: Outline of treatment patient will receive based on symptoms (SUD/ Mental Health)

### Appointment Data: Appointments for existing patients that new patients need to be scheduled around
-	APPOINTMENTID: unique key that represents an individual appointment
-	APPOINTMENTDATE: date of appointment
-	APPOINTMENTSTARTTIME: start time of appointment (local time)
-	APPOINTMENTDURATION: duration of each appointment (minutes)
-	PROVIDERID: unique key that represents an individual provider

### Provider State Data: States where each provider is licensed
-	PROVIDERID: unique key that presents an individual provider
-	STATE: state that the corresponding provider is available in

### Provider Schedule Data: Time slots where providers are available during the week
-	PROVIDERID: unique key that represents an individual provider
-	DAYOFWEEK: 1=Sunday, 7=Saturday
-	SLOTSTARTTIME: local time for the beginning of time slot
-	SLOTENDTIME: local time for end of time slot

## Rules
-	Do not make any time conversions, keep everything in local time
-	Each provider can only have 5 additional appointments per day
-	Appointments can only be scheduled between 8:30am and 9:00pm
-	Make sure that each provider is servicing patients from states that they are available according to the **Provider State Data** file

## Deliverables
-	Documentation on the following
  - Data engineering/preprocessing
  - Steps in algorithm 
-	Average & median time to first appointment from registration (hours) for patients in each PROGRAM
-	Average & median time to first appointment for all patients regardless of their PROGRAM

## Scoring Criteria (100 points total)
1. _(**10 for completion)_ Download data & load into IDE
2. _(**10 for completion, up to additional 10 for quality)_ Preprocess data into a modular back testing workflow: modular = can swap out algorithms to test easily
   * Iterate through all patients and show that a time slot is available for each patient that meets the following criteria
     * i.	Provider is eligible to provide care in state New Patient is from
     * ii.	New patient is placed in an open time slot that is not currently filled with an appointment in the Appointment Data file
   * $${\color{red}Upload\ your\ code\ into\ the\ items\\_2\\_3\ folder}$$
4.	_(**10 for completion, up to additional 10 for quality)_ Document steps for creating back testing workflow (numbered bullet points)
    * $${\color{red}Upload\ the\ document\ into\ the\ items\\_2\\_3\ folder}$$
6.	_(**10 for completion)_ Develop and test algorithm(s)
    * $${\color{red}Upload\ your\ code\ into\ the\ items\\_4\\_5\ folder}$$
8.	_(**10 for completion, up to additional 10 for quality)_ Document steps for algorithm(s) and testing (numbered bullet points)
    * $${\color{red}Upload\ the\ document\ into\ the\ items\\_4\\_5\ folder}$$
10.	_(**10 for completion, up to additional 10 for performance)_ Capture and present Mean & Median time to first appointment (TTFA)
  *	Break the Mean & Median values for TTFA using a graphical format (make sure that the exact values are labeled for the final output) into different groups based on the PROGRAM that the patient is in
    * i.	Combined
    * ii.	Mental Health
    * iii.	SUD
    * $${\color{red}Upload\ the\ document\ into\ the\ items\\_6\ folder}$$

$${\color{red}**IMPORTANT: \space all \space deliverables \space of \space 2,3,4,5,6 \space must \space be \space commited \space into \space your \space team \space repository \space \space by \space 2:00 \space PM**}$$

_**10 for completion:_ **this will be assessed throughout the day by our judges.**
