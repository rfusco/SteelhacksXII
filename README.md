https://devpost.com/software/elderguardian

# SteelhacksXII
Authors:
  Ryan Fusco
  Nate Kupec
  Bradley Zaricki

  ## Inspiration
We were inspired through personal experiences to create a protective software for elderly people on hospice or in retirement homes.

## What It Does

**ElderGuardian** is a discreet in-room device that continuously monitors conversations. It can distinguish between different voices and assign them to individual profiles. If concerning behavior or malpractice occurs, loved ones gain secure dashboard access to view transcribed recordings, complete with timestamps and speaker identification.

## How We Built It
ElderGuardian was built using **MongoDB**, **Flask**, and **React**.

## Challenges We Ran Into
The speaker diarization was very tricky to implement, as well as the language classifier and the dashboard.

## Accomplishments That We're Proud Of
Our database is fully connected to our frontend providing a seamless flow of information from recieved audio to the frontend dashboard.

## What We Learned
We learned about audio analysis, planning out design flows, and database tools.

## What's Next for ElderGuardian
The next step will be to implement a continous voice monitoring device to provide a full, shippable product.

Credit: https://github.com/MahmoudAshraf97/whisper-diarization
