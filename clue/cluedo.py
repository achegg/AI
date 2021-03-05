'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***"

    clauses = []
    for card in cards:
        clauses.append([Cluedo.getIdentifierFromNames(hand, card)])

    return clauses

def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """
    "*** YOUR CODE HERE ***"
    exists = []
    clause = []
    for card in Cluedo.cards:
        clause.clear()
        for hand in Cluedo.hands:
            clause.append(Cluedo.getIdentifierFromNames(hand, card))
        exists.append(clause)
    return exists

def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    clauses = []
    for card in Cluedo.cards:
        for hand in Cluedo.hands:
            for hand2 in Cluedo.hands:
                if hand != hand2:
                    id1 = -1 * Cluedo.getIdentifierFromNames(hand, card)
                    id2 = -1 * Cluedo.getIdentifierFromNames(hand2, card)
                    clauses.append([id1, id2])


    return clauses

def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    clause = []
    case = []
    for suspect in Cluedo.suspects:
        clause.append(Cluedo.getIdentifierFromNames("cf", suspect))
    case.append(clause)
    clause.clear()
    for weapon in Cluedo.weapons:
        clause.append(Cluedo.getIdentifierFromNames("cf", weapon))
    case.append(clause)
    clause.clear()
    for room in Cluedo.rooms:
        clause.append(Cluedo.getIdentifierFromNames("cf", room))
    case.append(clause)
    return case

def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"
    clause = []
    for s1 in Cluedo.suspects:
        for s2 in Cluedo.suspects:
            if s1 != s2:
                id1 = -1 * Cluedo.getIdentifierFromNames("cf", s1)
                id2 = -1 * Cluedo.getIdentifierFromNames("cf", s2)
                clause.append([id1, id2])
    for w1 in Cluedo.weapons:
        for w2 in Cluedo.weapons:
            if w1 != w2:
                id1 = -1 * Cluedo.getIdentifierFromNames("cf", w1)
                id2 = -1 * Cluedo.getIdentifierFromNames("cf", w2)
                clause.append([id1, id2])
    for r1 in Cluedo.rooms:
        for r2 in Cluedo.rooms:
            if r1 != r2:
                id1 = -1 * Cluedo.getIdentifierFromNames("cf", r1)
                id2 = -1 * Cluedo.getIdentifierFromNames("cf", r2)
                clause.append([id1, id2])

    return clause

def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    clause = []
    if refuter is None:
        for player in Cluedo.suspects:
            if player is not suggester:
                clause.append([-1 * Cluedo.getIdentifierFromNames(player, card1)])
                clause.append([-1 * Cluedo.getIdentifierFromNames(player, card2)])
                clause.append([-1 * Cluedo.getIdentifierFromNames(player, card3)])
        return clause
    elif cardShown is None:
        i = Cluedo.suspects.index(suggester) + 1
        if i == len(Cluedo.suspects):
            i = 0
        while Cluedo.suspects[i] != refuter:
            clause.append([-1 * Cluedo.getIdentifierFromNames(Cluedo.suspects[i], card1)])
            clause.append([-1 * Cluedo.getIdentifierFromNames(Cluedo.suspects[i], card2)])
            clause.append([-1 * Cluedo.getIdentifierFromNames(Cluedo.suspects[i], card3)])

            i += 1
            if i == len(Cluedo.suspects):
                i = 0
        id1 = Cluedo.getIdentifierFromNames(refuter, card1)
        id2 = Cluedo.getIdentifierFromNames(refuter, card2)
        id3 = Cluedo.getIdentifierFromNames(refuter, card3)
        clause.append([id1, id2, id3])
        return clause
    else:
        i = Cluedo.suspects.index(suggester) + 1
        if i == len(Cluedo.suspects):
            i = 0
        while Cluedo.suspects[i] != refuter:
            clause.append([-1 * Cluedo.getIdentifierFromNames(Cluedo.suspects[i], card1)])
            clause.append([-1 * Cluedo.getIdentifierFromNames(Cluedo.suspects[i], card2)])
            clause.append([-1 * Cluedo.getIdentifierFromNames(Cluedo.suspects[i], card3)])

            i += 1
            if i == len(Cluedo.suspects):
                i = 0
        clause.append([Cluedo.getIdentifierFromNames(refuter, cardShown)])
        return clause

def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    clause = []
    id1 = Cluedo.getIdentifierFromNames("cf", card1)
    id2 = Cluedo.getIdentifierFromNames("cf", card2)
    id3 = Cluedo.getIdentifierFromNames("cf", card3)

    if correct:
        clause.append([id1])
        clause.append([id2])
        clause.append([id3])
        return clause

    clause.append([-id1, -id2, -id3])

    acc1 = Cluedo.getIdentifierFromNames(accuser, card1)
    acc2 = Cluedo.getIdentifierFromNames(accuser, card2)
    acc3 = Cluedo.getIdentifierFromNames(accuser, card3)
    clause.append([-acc1])
    clause.append([-acc2])
    clause.append([-acc3])

    return clause
