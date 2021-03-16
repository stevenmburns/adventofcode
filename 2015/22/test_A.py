import copy
import pytest
import itertools
from collections import defaultdict, deque
import logging

#logging.basicConfig(level=logging.INFO)


class Effect:
    def __init__(self, nm, timer, *, armor=0, damage=0, heals=0, mana=0):
        self.nm = nm
        self.timer = timer
        self.armor = armor
        self.damage = damage
        self.heals = heals
        self.mana = mana

class Player:
    def __init__(self, hitpoints, mana):
        self.hitpoints = hitpoints
        self.mana = mana
        self.armor = 0
        self.effects = []

    def summary(self):
        logging.info( f'- Player has {self.hitpoints} hit points, {self.armor} armor, {self.mana} mana')

    def cleanup(self):
        effects = []
        for effect in self.effects:
            if effect.timer > 0:
                effects.append(effect)
            else:
                logging.info( f'{effect.nm} wears off.')
                if effect.nm == 'Shield':
                    self.armor = 0
        self.effects = effects

    def process_effects(self, boss):
        for effect in self.effects:
            effect.timer -= 1
            if effect.damage > 0:
                logging.info( f'{effect.nm} deals {effect.damage} damage; its timer is now {effect.timer}')
                boss.hitpoints -= effect.damage
            if effect.mana > 0:
                logging.info( f'{effect.nm} provides {effect.mana} mana; its timer is now {effect.timer}')
                self.mana += effect.mana
            if effect.armor > 0:
                self.armor = effect.armor

        self.cleanup()

class Boss:
    def __init__(self, hitpoints, damage): 
        self.hitpoints = hitpoints
        self.damage = damage

    def summary(self):
        logging.info( f'- Boss has {self.hitpoints} hit points')

hard = True

def player_step( spell, player, boss):

    if hard:
        player.hitpoints -= 1
        if player.hitpoints <= 0:
            return 'boss'

    logging.info( f'')
    logging.info( f'-- Player turn --')
    player.summary()
    boss.summary()

    player.process_effects( boss)

    if boss.hitpoints <= 0:
        return 'player'

    spell_nm, spell_mana_cost, effect = spell

    if effect.nm in ( e.nm for e in player.effects):
        logging.info( f'Illegal move')
        return 'boss'

    player.mana -= spell_mana_cost
    if player.mana < 0:
        logging.info( f'Negative mana---illegal move')
        return 'boss'

    if effect.timer is None:
        if effect.damage > 0:
            boss.hitpoints -= effect.damage
        if effect.heals > 0:
            player.hitpoints += effect.heals
        logging.info( f'Player casts {spell_nm}, dealing {effect.damage} damage, healing {effect.heals}')
    else:
        logging.info( f'Player casts {spell_nm}')
        player.effects.append(copy.copy(effect))

    if boss.hitpoints <= 0:
        return 'player'

    return 'neither'

def boss_step( boss, player):

    logging.info( f'')
    logging.info( f'-- Boss turn --')
    player.summary()
    boss.summary()

    player.process_effects(boss)

    if boss.hitpoints <= 0:
        return 'player'

    d = max( 1, boss.damage - player.armor)
    logging.info( f'Boss attacks for {d}.')
    player.hitpoints -= d

    if player.hitpoints <= 0:
        return 'boss'

    return 'neither'

def game( spell_tbl, seq):
    rc = 'neither'
    player = Player( hitpoints=50, mana=500)
    boss = Boss( hitpoints=51, damage=9)
    for s in seq:
        rc = player_step( spell_tbl[s], player, boss)
        if rc != 'neither':
            break
        rc = boss_step( boss, player)
        if rc != 'neither':
            break

    return rc


def main():
    spells = [ ('Magic Missile', 53, Effect( 'Magic Missile', None, damage=4)),
               ('Drain', 73, Effect( 'Drain', None, damage=2, heals=2)), 
               ('Shield', 113, Effect( 'Shield', 6, armor=7)),
               ('Poison', 173, Effect( 'Poison', 6, damage=3)),
               ('Recharge', 229, Effect('Recharge', 5, mana=101))]

    spell_tbl = { p[0]: p for p in spells}

    if True:
        seqs = itertools.product( spell_tbl.keys())

        winning_seqs = []

        for level in range(15):

            tied_seqs = []            
            for seq in seqs:
                rc = game( spell_tbl, seq)
                if rc == 'player':
                    winning_seqs.append( seq)
                elif rc == 'neither':
                    tied_seqs.append( seq)

            new_seqs = []
            for seq in tied_seqs:
                for spell_nm in spell_tbl.keys():
                    new_seq = seq + (spell_nm,)
                    new_seqs.append(new_seq)

            seqs = new_seqs

            best = None
            best_seq = None
            for seq in winning_seqs:
                cost = sum(spell_tbl[nm][1] for nm in seq)
                if best is None or best > cost:
                    best = cost
                    best_seq = seq
            print( level, len(seqs), len(winning_seqs), best, best_seq)

    else:
        seq = ['Poison', 'Magic Missile', 'Recharge', 'Poison', 'Shield', 'Recharge', 'Poison', 'Drain']
        print( game(spell_tbl, seq))
    
    return 0

#@pytest.mark.skip
def test_B():
    print(main())

