ScriptVersion = "0.0.1alpha"
# Very unstable alpha Version!

# Locally include and use packages
if isdefined(@__MODULE__, :LookUpTable)
    LookUpTable isa Module || error("LookUpTable is present and it is not a Module")
else
    include("LookUpTable.jl")
end
using .LookUpTable

if isdefined(@__MODULE__, :FileCodeOutput)
    FileCodeOutput isa Module || error("FileCodeOutput is present and it is not a Module")
else
    include("FileCodeOutput.jl")
end
using .FileCodeOutput

if isdefined(@__MODULE__, :JSONPhraser)
    JSONPhraser isa Module || error("JSONPhraser is present and it is not a Module")
else
    include("JSONPhraser.jl")
end
using .JSONPhraser

#=======================User configured Section==========================#
# Your Version Number
YourVersion= "0.1"

# C(suitable for C and C++),Julia
codeStyle = "C"

#=======================User configured Section==========================#

M1=ReliAffixECDConverter();
M2=ReliLevelECDConverter();

open("output.txt", "w") do file
    PrintScriptVersion(file, ScriptVersion, YourVersion;codeStyle=codeStyle);
    Print3DMatrix(file, M1 ; varName="reliSubstat",codeStyle=codeStyle);
    Print3DMatrix(file, M2 ; varName="reliMainstat",codeStyle=codeStyle);
end