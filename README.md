**part1_unmatched.py:** Apart from deleting the penalty part, nothing has changed in the code section.

But now Part 1, which is the unmatched order in market orders, only represents predictions/assumptions. These
are not real grid transactions yet - real grid settlement occurs in Part 2, after the real deviation is resolved.

It can be used to compare the forecast settlement results and actual settlement result. If you don't need to know the forecasted  results, you can also delete part 1

**part2_deviation.py:** Before internal matching, offset the deviation with the unmatched amount of the 
household's daily market (to avoid unnecessary grid trading)

The current logic is that when actual electricity consumption/generation data is available, there is a 
discrepancy (surplus or shortfall) between each user's actual and planned data. The Balancing Operator 
processes these deviations in three steps: first, offset the deviation with the Household's own daily 
unmatched amount (to avoid unnecessary grid transactions); The remaining deviation will be matched through 
P2P within the community (surplus users will be sold to short users and settled at internal prices); The 
final unresolved part is truly traded with the power grid, resulting in actual fund settlement.

main.py:

