import Coin_Toss as Cls
import scr.FormatFunctions as Format
import scr.FigureSupport as Figs
import scr.StatisticalClasses as Stat

PROBABILITY_HEADS = 0.5  # probability of getting heads
COIN_EFFECT_RATIO = 0.9  # ratio of the unfair coin (0.45) to the fair coin (0.50)

REAL_N_GAMES = 10        # simulation length of the real cohort to make the projections for
NUM_SIM_GAMES = 1000     # number of simulated cohorts used for making projections
ALPHA = 0.05             # significance level


# expected rewards with a fair coin
multiSetsOfFairGames = Cls.MultipleGameSets(
    ids=range(NUM_SIM_GAMES),
    prob_head=[PROBABILITY_HEADS] * NUM_SIM_GAMES,
    n_games_in_a_set= [REAL_N_GAMES] * NUM_SIM_GAMES)
multiSetsOfFairGames.simulation()

# expected rewards with an unfair coin
multiSetsOfUnfairGames = Cls.MultipleGameSets(
    ids=range(NUM_SIM_GAMES, 2* NUM_SIM_GAMES),
    prob_head=[PROBABILITY_HEADS*COIN_EFFECT_RATIO] * NUM_SIM_GAMES,
    n_games_in_a_set= [REAL_N_GAMES] * NUM_SIM_GAMES)
multiSetsOfUnfairGames.simulation()

def print_outcomes(sim_reward, strategy_name):
    """ prints the outcomes of a simulated set of games under transient state
    :param sim_output: output of a simulated cohort
    :param strategy_name: the name of the selected coin
    """

    # mean and confidence interval text of rewards
    reward_mean_CI_text = Format.format_estimate_interval(
        estimate=sim_reward.get_mean_total_reward(),
        interval=sim_reward.get_PI_total_reward(alpha=ALPHA),
        deci=1)

    # print reward statistics
    print(strategy_name)
    print("  Estimate of mean reward and {:.{prec}%} prediction interval:".format(1 - ALPHA, prec=0),
          reward_mean_CI_text)

def histograms(sim_output_fair_coin, sim_output_unfair_coin):
    """ draws the survival curves and the histograms of rewards
        :param sim_output_fair_coin: output of a set of games simulated with a fair coin
        :param sim_output_unfair_coin: output of a set of games simulated with an unfair coin
    """

    # histograms of rewards
    set_of_rewards = [
        sim_output_fair_coin.get_all_total_rewards(),
        sim_output_unfair_coin.get_all_total_rewards()
    ]


    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_rewards,
        title="Histogram of Rewards from 1000 Games obtained from the transient-state simulation model",
        x_label="Game Rewards",
        y_label="Frequency",
        bin_width=25,
        legend=['Fair Coin', 'Unfair Coin'],
        transparency=0.5
    )


def print_comparative_outcomes(sim_output_fair_coin, sim_output_unfair_coin):
    """ prints expected change from unfair coin
        :param sim_output_fair_coin: output of a set of games simulated with a fair coin
        :param sim_output_unfair_coin: output of a set of games simulated with an unfair coin
    """

    # change in reward
    increase = Stat.DifferenceStatIndp(
        name='Change in reward',
        x=sim_output_unfair_coin.get_all_total_rewards(),
        y_ref=sim_output_fair_coin.get_all_total_rewards()
    )
    # estimate and CI
    estimate_CI = Format.format_estimate_interval(
        estimate=increase.get_mean(),
        interval=increase.get_t_CI(alpha=ALPHA),
        deci=1
    )
    print("Average change in mean reward and {:.{prec}%} prediction interval:".format(1 - ALPHA, prec=0),
          estimate_CI)


# print outcomes of each cohort
print_outcomes(multiSetsOfFairGames, 'When the coin is fair:')
print_outcomes(multiSetsOfUnfairGames, 'When the coin is unfair:')

# print comparative outcomes
print_comparative_outcomes(multiSetsOfFairGames, multiSetsOfUnfairGames)

# draw survival curves and histograms
histograms(multiSetsOfFairGames, multiSetsOfUnfairGames)
