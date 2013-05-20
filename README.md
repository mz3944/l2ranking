L2Ranking
=========
**L2Ranking** projekt je nadgradnja že obstoječe spletne strani (l2ranking.com), ki bo vsebovala seznam privatnih Lineage 2 strežnikov s podrobnimi informacijami, omogočala glasovanje igralcev za njihov strežnik ter napredno iskanje igralnih strežnikov glede na željene lastnosti. Spletna stran bo tudi omogočala nagrajevanje igralcev za glasovanje na igralnem strežniku. Stran bo omogočala registracijo preko socialnih omrežji kot so Facebook, Twitter in Google+. Možen bo tudi nakup Premium Membership, ki bo izpostavil uporabnikov igralni strežnik in tako omogočil bolj izpostavljeno oglaševanje. Na spletni strani bodo vidni tudi premiki igralnih strežnikov po lestvici ter statistike ogledov, glasovanja in podobno.


## Models:

* Server
* Category
* Review
* Vote
* News

## Views:
###  Basic

* Homepage `/`
* Server Listing `/servers/`
* Server Details `/server/<id>/`
* Vote for Server `/server/vote/<id>/`
  
### User Panel

* User Servers `/servercp/`
* User Add Server `/servercp/add/`
* User Edit Server `/servercp/update/<id>/`
* User Delete Server `/servercp/delete/<id>/`
* User Server Statistics `/servercp/info/<id>/`
* User Registration `/usercp/register/`
* User Login `usercp/login/`
* User Password Reset `usercp/password/reset/`
* User Account Details `/usercp/account/`

## Plugins

* Django Social (Integrate with Facebook, Google+ & Twitter)
* Django Paypal (Buy Gold Membership via Paypal)
* Django Adscaptcha (Does not yet exist - anti-bot measure on voting page)

## Other Features

* Dynamic Signatures (generates PNG based on server information such as Chronicle, EXP, SP etc.)
* Server Movement (shows previous rank - for example last week)
* Server News + Widget (Displays server news managed by user on Server Details page, user can also use javascript code to display news on server site - remote)
* Vote reward system (user can request reward ingame - server validates vote by sending request to website)
* Server status checker (website checks either server is online or offline)
* Responsive design (design changed based on viewpoint - PC, Tablet, Smartphone)
