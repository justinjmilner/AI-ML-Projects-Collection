
I started with the global variable values provided in the default python code and used the neural
network model that was desplayed in the lecture. My accuracy was around 90% and loss around 45%. I Tried
the same NN model with no dropout, 0.1 dropout, and 0.25 dropout. The results didn't make much difference.

I tried increasing the amount of filters and increasing the kernal size for the CONV layer. I found that
as I increased the number of filters the model took longer to train, but gained accuracy. With too many
filters I found that the model became overfitted which resulted in high training accuracy but low
test accuracy. I tried increasing pooling but found that 2,2 gave the best results for this case.
I increased the number of filter layers and pooling and found that improves my results.
I increased the number of units next in my dense hidden layer. I found that accuracy decreased as I
increased the nodes. I believe this is because I had 2 conv and 2 pooling layers so there wasnt enough
data to train the extra units without become overfitted. I tried different activation functions and
found that relu worked best for my experiemental model. Next I experimented with dropout values of 0.1,
0.25 and 0.5. 0.25 gave the best results. Next I tried increasing the epochs. I found 10-20 was a good
fit for my model where the computing was reasonable for the benefits, and the model showed good levels
of generalization and fitting. Lastly I tried changing the photo dimensions to 60x60. I found that
I was able to improve the model but it took longer to train. By increasing the number of filters I was
able to reduce training time and still maintain the improved results.

After all I did some research to experiment with professionally made CNN's for this specific CV task.
I came across the LeNet5 model, which I implemented in my code and played around with the features. I found
that the default settings of LeNet5 provided better results than anything I could fine tune on my own.
Lastly I implemented a modified version of LeNet5, which I linked in the description of my project video.
The model had improved accuracy and loss compared to LeNet5. I also tried to fine tune this model by playing
with the inputs. I was unable to increase performance for the model by changing any parameters.

My key takeaway is that a well trained model needs to have the right amount of complexity to delegate the
incoming data properly, and to balance the scale of the model and data with computing time. I also
realize the amount of expertise required to discover parameters that can improve upon well known models.