# MageHand

## Helpfull Callback Information

### Booting Phase
![booting flowchart](images/booting.png)
### Introduction Phase
![introduction flowchart](images/introduction.png)
- *Summary:*

1 callback: ["Stop"]

### Confirmation Phase
![confirmation flowchart](images/confirmation.png)
- *Summary:*

2 callbacks: ["None", "ThumbsUp"]

1 confirmation callback: ["None"]

### Selection Phase
![selection flowchart](images/selection.png)
- *Summary:*

4 callbacks: ["Undefined", "None", "ThumbsUp", "ThumbsDown"]

3 confirmation callbacks: ["ThumbsUp", "ThumbsDown", "None"]

### Pouring Phase
![pouring flowchart](images/pouring.png)
- *Summary:*

5 callbacks: ["ThumbsDown", "Fist", "Undefined", "Stop", "None"]

3 confirmation callbacks: ["ThumbsDown", "Stop", "None"]

### Decision Phase
![decision flowchart](images/decision.png)

- *Summary:*

4 callbacks: ["ThumbsDown", "ThumbsUp", "Peace", "None"] *!!! ThumbsDown, ThumbsUp e Peace são a mesma função*

4 confirmation callbacks: ["ThumbsDown", "ThumbsUp", "Peace", "None"]
### Payment Phase
![payment flowchart](images/payment.png)

- *Summary:*

1 callback: ["ThumbsDown"]

1 confirmation callback: ["ThumbsDown"]
