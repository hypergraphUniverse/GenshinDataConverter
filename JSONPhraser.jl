# Convert json Data form Dimbreath/GenshinData into Matrix/Array

module JSONPhraser
export ReliAffixECDConverter,ReliLevelECDConverter

using JSON

if isdefined(@__MODULE__, :LookUpTable)
    VectorFunctions isa Module || error("LookUpTable is present and it is not a Module")
else
    include("LookUpTable.jl")
end
using .LookUpTable

# Convert ReliquaryAffixExcelConfigData.json into Matrix
# Substat of Artifacts
function ReliAffixECDConverter()

    # Read form JSON File
    dict = Dict()
    open("ReliquaryAffixExcelConfigData.json", "r") do f
        dict=JSON.parse(f)  # parse and transform data
    end

    # Initialize with empty Array
    # Rank, Substats, Sequence
    dataSet=fill(0f0,5,length(LookUpTable.substatProject),4);

    # fill in the data
    for i in 1:length(dict)
    
        # read ID for identification
        this_id=string(dict[i]["Id"]);
        this_rank=parse(Int64,this_id[1]);
        this_seq=parse(Int64,this_id[6]);
        # ID e.g. 501244 first digit is Rank, last digit is The Sequence Number in same substat

        # Skip the 9xxxxxx ID
        if !(1<=this_rank<=5)
            continue;
        end

        # Skip the Substat not covered in LookUpTable.substatProject
        if !SubstatHasKey(dict[i]["PropType"])
            continue;
        end

        # Sort Data
        dataSet[ this_rank, SubstatLookUp(dict[i]["PropType"]), this_seq ] = dict[i]["PropValue"];
        end
    return dataSet
end

# Convert ReliquaryLevelExcelConfigData.json into Matrix
# Mainstat of Artifacts
function ReliLevelECDConverter()
    dict = Dict()

    # Read form JSON File
    open("ReliquaryLevelExcelConfigData.json", "r") do f
        dict=JSON.parse(f)  # parse and transform data
    end

    # Rank, Substats, Level
    dataSet=fill(0f0,5,length(LookUpTable.mainstatProject),21);

    for i in 1:length(dict)
    
        # Skip the Data with no rank
        if !(haskey(dict[i],"Rank"))
            continue;
        end

        # Sort Data
        for j in 1:length(dict[i]["AddProps"])
            # Skip the Mainstat not covered in LookUpTable.mainstatProject
            if !MainstatHasKey(dict[i]["AddProps"][j]["PropType"])
                continue;
            end
            dataSet[ dict[i]["Rank"], MainstatLookUp(dict[i]["AddProps"][j]["PropType"]), dict[i]["Level"] ] = dict[i]["AddProps"][j]["Value"];
        end
    end
    return dataSet
end

end