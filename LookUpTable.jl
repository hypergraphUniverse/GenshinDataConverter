module LookUpTable

export SubstatHasKey,SubstatLookUp,MainstatHasKey,MainstatLookUp

#=================user configured section===================#

# Please add your output substat Sequence that you wish
substatProject=Dict(
    "hp"=>1, 
    "hp_percent"=>2,
    "attack"=>3,
    "attack_percent"=>4,
    "defence"=>5,
    "defence_percent"=>6, 
    "charge_efficiency"=>7, 
    "element_mastery"=>8,
    "critical"=>9,
    "critical_hurt"=>10,
)

# Please add your output mainstat Sequence that you wish
mainstatProject=Dict(
    "hp"=>1,
    "hp_percent"=>2,
    "attack"=>3,
    "attack_percent"=>4,
    "defence"=>5,
    "defence_percent"=>6,
    "critical"=>7,
    "critical_hurt"=>8,
    "charge_efficiency"=>9,
    "heal_add"=>10,
    "element_mastery"=>11,
    "fire_add_hurt"=>12,
    "elec_add_hurt"=>13,
    "water_add_hurt"=>14,
    "wind_add_hurt"=>15,
    "rock_add_hurt"=>16,
    "ice_add_hurt"=>17,
    "physical_add_hurt"=>18,
)


#==============end of user configured section===============#

# constant look-up table

statIntern=Dict(
    "FIGHT_PROP_HP"=>"hp",
    "FIGHT_PROP_HP_PERCENT"=>"hp_percent",
    "FIGHT_PROP_ATTACK"=>"attack",
    "FIGHT_PROP_ATTACK_PERCENT"=>"attack_percent",
    "FIGHT_PROP_DEFENSE"=>"defence",
    "FIGHT_PROP_DEFENSE_PERCENT"=>"defence_percent",
    "FIGHT_PROP_CRITICAL"=>"critical",
    "FIGHT_PROP_CRITICAL_HURT"=>"critical_hurt",
    "FIGHT_PROP_CHARGE_EFFICIENCY"=>"charge_efficiency",
    "FIGHT_PROP_HEAL_ADD"=>"heal_add",
    "FIGHT_PROP_ELEMENT_MASTERY"=>"element_mastery",
    "FIGHT_PROP_FIRE_ADD_HURT"=>"fire_add_hurt",
    "FIGHT_PROP_ELEC_ADD_HURT"=>"elec_add_hurt",
    "FIGHT_PROP_WATER_ADD_HURT"=>"water_add_hurt",
    "FIGHT_PROP_WIND_ADD_HURT"=>"wind_add_hurt",
    "FIGHT_PROP_ROCK_ADD_HURT"=>"rock_add_hurt",
    "FIGHT_PROP_GRASS_ADD_HURT"=>"grass_add_hurt",
    "FIGHT_PROP_ICE_ADD_HURT"=>"ice_add_hurt",
    "FIGHT_PROP_PHYSICAL_ADD_HURT"=>"physical_add_hurt",
    "FIGHT_PROP_FIRE_SUB_HURT"=>"fire_sub_hurt",
);

function SubstatHasKey(s::String)
    return haskey(substatProject,statIntern[s])
end

function SubstatLookUp(s::String)
    return substatProject[statIntern[s]]
end

function MainstatHasKey(s::String)
    return haskey(mainstatProject,statIntern[s])
end

function MainstatLookUp(s::String)
    return mainstatProject[statIntern[s]]
end

end