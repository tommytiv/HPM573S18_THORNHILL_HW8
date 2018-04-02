import Coin_Toss as Cls

# expected rewards from 1000 games
setOfGames = Cls.SetOfGames(id=1, prob_head=0.5, n_games=1000)
outcomes = setOfGames.simulation()

##### Problem 1 #####
print("Estimated expected reward:", outcomes.get_ave_reward())
print("The 95% CI of expected reward:", outcomes.get_CI_reward(0.05))

print("Probability of loss in a single game:", outcomes.get_prob_loss())
print("The 95% CI of loss probability:", outcomes.get_CI_probLoss(0.05))

##### Problem 2 #####
print("If we run our simulation many times, "
      "on average 95% of the confidence intervals generated will capture the true mean.")

