import Coin_Toss as Cls
import scr.FormatFunctions as Format
import scr.FigureSupport as Figs
import scr.StatisticalClasses as Stat
import Parameters as P


PROBABILITY_HEADS = 0.5  # probability of getting heads
COIN_EFFECT_RATIO = 0.9  # ratio of the unfair coin (0.45) to the fair coin (0.50)

N_GAMES = 1000      # simulation length
ALPHA = 0.05        # significance level

# expected rewards with a fair coin
setOfFairGames = Cls.SetOfGames(
    id=1,
    prob_head=PROBABILITY_HEADS,
    n_games=N_GAMES)
fairOutcomes = setOfFairGames.simulation()

# expected rewards with an unfair coin
setOfUnfairGames = Cls.SetOfGames(
    id=2,
    prob_head=PROBABILITY_HEADS*COIN_EFFECT_RATIO,
    n_games=N_GAMES)
unfairOutcomes = setOfUnfairGames.simulation()

def print_outcomes(sim_reward, strategy_name):
    """ prints the outcomes of a simulated cohort under steady state
    :param sim_output: output of a simulated cohort
    :param strategy_name: the name of the selected coin
    """

    # mean and confidence interval text of patient survival time
    reward_mean_CI_text = Format.format_estimate_interval(
        estimate=sim_reward.get_ave_reward(),
        interval=sim_reward.get_CI_reward(alpha=P.ALPHA),
        deci=1)

    # print survival time statistics
    print(strategy_name)
    print("  Estimate of mean reward and {:.{prec}%} confidence interval:".format(1 - P.ALPHA, prec=0),
          reward_mean_CI_text)

def histograms(sim_output_fair_coin, sim_output_unfair_coin):
    """ draws the survival curves and the histograms of rewards
     :param sim_output_fair_coin: output of a cohort simulated with fair coin
    :param sim_output_unfair_coin: output of a cohort simulated with unfair coin
    """

    # histograms of survival times
    set_of_rewards = [
        sim_output_fair_coin.get_rewards(),
        sim_output_unfair_coin.get_rewards()
    ]


    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_rewards,
        title="Histogram of Rewards from 1000 Games obtained from the steady-state simulation model",
        x_label="Game Rewards",
        y_label="Frequency",
        bin_width=25,
        legend=['Fair Coin', 'Unfair Coin'],
        transparency=0.5
    )


def print_comparative_outcomes(sim_output_fair_coin, sim_output_unfair_coin):
    """ prints expected change from unfair coin
    :param sim_output_fair_coin: output of a cohort simulated with fair coin
    :param sim_output_unfair_coin: output of a cohort simulated with unfair coin
    """

    # change in reward
    increase = Stat.DifferenceStatIndp(
        name='Change in reward',
        x=sim_output_unfair_coin.get_rewards(),
        y_ref=sim_output_fair_coin.get_rewards()
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=ALPHA),
        deci=1
    )
    print("Average increase in mean reward and {:.{prec}%} confidence interval:".format(1 - P.ALPHA, prec=0),
          estimate_CI)


# print outcomes of each cohort
print_outcomes(fairOutcomes, 'When coin is fair:')
print_outcomes(unfairOutcomes, 'When coin is unfair:')

# print comparative outcomes
print_comparative_outcomes(fairOutcomes, unfairOutcomes)

# draw survival curves and histograms
histograms(fairOutcomes, unfairOutcomes)

