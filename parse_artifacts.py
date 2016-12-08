#!/usr/bin/python
import itertools




class Artifact:
    def __init__(self):
        self.base_name = "no base name"
        self.qualified = "no qualifier"
        self.description = ""
        self.symbol = "No symbol defined"
        self.item_type = "No item type defined"
        self.color = "No color defined"
        self.flags = []
        self.values = []
#        print "hello world"
        
    def __str__(self):
        description =  "Artifact Name: %s %s\n" % (self.base_name,self.qualifier)
        description += "Type = %s\n" % self.item_type
        description += "Symbol = %s\n" % self.symbol
        description += "Color = %s\n" % self.color
        description += "Flags = %s\n" % self.flags
        description += "Values = %s\n" % self.values
        description += "Item Description = \n%s\n" % self.description
        return description

    def resistances(self):
        resistances = []
        for attribute in self.values:
            if ("RES" in attribute):
                resistances.append(attribute)

        return resistances

    def good(self):
        flag_exclusions = ["AGGRAVATE","LIGHT_CURSE","HEAVY_CURSE","PERMA_CURSE"]
        for flag in self.flags:
            if flag in flag_exclusions: return False
        return True

def check_combos(items):
    armours = []
    weapons = []
    amulets = []
    helmets = []
    gloves = []
    lights = []
    rings = []
    shields = []
    boots = []
    bows = []

    #seperate out equipment by type
    for item in items:
#        print "ITEM: %s" % item
        if ("armour" in item.item_type):
            armours.append(item)
        elif (item.item_type == "amulet"):
           amulets.append(item)
        elif (item.item_type == "bow"):
            bows.append(item)
        elif (item.item_type == "gloves"):
            gloves.append(item)
        elif (item.item_type == "light"):
            lights.append(item)
        elif (item.item_type == "ring"):
            rings.append(item)
        elif (item.item_type == "boots"):
            boots.append(item)
        elif (item.item_type == "shield"):
            shields.append(item)
        elif (item.item_type in ["sword","polearm","hafted"]):
            weapons.append(item)
        elif (item.item_type in ["crown","helm"]):
           helmets.append(item)

    #calculate all ring combinations for two rings       
    ring_combos = itertools.combinations(rings,2)

  #  for rings in ring_combos:
   #     print type(rings)
    #    print type(ring_combos)
        #print "Ring1: %s\nRing2: %s\n\n" % (rings[0].qualifier,rings[1].qualifier)
        
    
    combos = itertools.product(armours,weapons,amulets,helmets,gloves,ring_combos,shields,boots,bows)
    #for item in combos:
     #     print item

    
    max_coverage = 0  #maximum number of flags/resists found so far
    best_combos = []  #stores all combinations of equipment with max coverage 

    
    total_coverage = 0 

    for combo in combos:
         valflag = []  #stores unignored resists/flags for equipment set 
         for item in combo:
             #first clause of IF statement deals with ring combinations, second clause deals with all other artifacts
             if (not isinstance(item,Artifact)):
                 valflag += item[0].flags + item[0].resistances() + item[1].flags + item[1].resistances()
             else:
                 valflag += item.flags+item.resistances()

         total_coverage = len(set(valflag))

         values = set(valflag) #get only unique resists/flags for equipment and store them in values

         if (total_coverage > max_coverage):
             max_coverage = total_coverage
             best_combos = []
             best_combos.append([values,combo])  #store combination of equipment as well as the actual resists/flags in a set

         elif (total_coverage == max_coverage):
             best_combos.append([values,combo])
         
             
    print "Best equipment combinations are:\n"


    for combo in best_combos:
#        print "\n==========\n"
        for item in combo[1]:
            #First part of IF statement deals with printing out ring combinations, second part deals all other artifacts
            if (not isinstance(item,Artifact)):
                print "Ring1: %s %s\n" % (item[0].base_name,item[0].qualifier)
                print "Ring2: %s %s\n" % (item[1].base_name,item[1].qualifier)
            else:
                print "%s: %s %s\n" % (item.item_type, item.base_name,item.qualifier)        

        print "Valflag:\n%s\nNumber of flags/resists = %d" % (combo[0], len(combo[0]))
        print "\n==========\n"
        
    # for array in [armours,weapons,amulets,helmets,gloves,lights,rings,shields,boots]:
    #     print "%s\n============\n" % array[0]
    #     for item in array[1:]:
    #         print item
    print "Total number of combinations found: %d" % len(best_combos)
    
    

with open("artifact_test.txt") as artifact_file:

    description_flag = False
    artifacts = []

    #items with properties I do not want to include

    flag_ignore = ["SLOW_DIGEST","FEATHER"]
    
    for line in artifact_file:
        #skip commented and blank lines
        if (line[0] == "#" or line.strip() == ""):

            #if multiline description flag is True, flip it as the description has ended
            if (description_flag):
                description_flag = False
                artifacts.append(cur_artifact)
                description = ""
            continue

        #seperate the fields
        fields = line.split(":") 

        #get the field name from the file
        field_name = fields[0]

        
        if (field_name == "name"):
            cur_artifact = Artifact()
            cur_artifact.qualifier = fields[2].strip()
            
        elif (field_name  == "base-object"):
            cur_artifact.item_type = fields[1].strip()
            cur_artifact.base_name = fields[2].strip()

        elif (field_name  == "graphics"):
            cur_artifact.symbol = fields[1].strip()
            cur_artifact.color = fields[2].strip()

        elif (field_name  == "info"):
            cur_artifact.item_level = fields[1].strip()
            cur_artifact.weight = fields[2].strip()

#        elif (field_name  == "type"):
 #           cur_artifact.item_type = fields[1].strip()
            
        elif (field_name  == "flags"):
            flags_flag = True
            temp_flags =  fields[1].strip().split("|")

            #stripping out whitespaces before adding to artifact flags
            for flag in temp_flags:
                stripped_flag = flag.strip()
                if (stripped_flag and stripped_flag not in flag_ignore):
                    cur_artifact.flags.append(stripped_flag)

        elif (field_name == "values"):
            values_flag = True
            temp_values =  fields[1].strip().split("|")

            #stripping out whitespaces before adding to artifact flags
            for value in temp_values:
                stripped_value = value.strip()
                if (stripped_value):
                    cur_artifact.values.append(stripped_value)
                    
        elif (field_name  == "desc"):
            #finished reading multiline flags
            if (flags_flag):
                flags_flag = False
                
            description_flag = True
            cur_artifact.description += fields[1].lstrip()

    flags=[]
#    for artifact in artifacts:
#        flags +=  artifact.flags
#        for value in artifact.values:
#            if ("RES" in value and "[3]" in value):
#                print artifact
 #               break



#    good_artifacts = [artifact for artifact in artifacts if artifact.flags not in flag_exclusions]


    good_artifacts = []

    for artifact in artifacts:
        if artifact.good():
            good_artifacts.append(artifact)
        

    # for artifact in artifacts:
    #     print artifact
    
    #print set(flags)

#    demo = [1,3,5,7]
#    demo2 = [1,3,5,7]


#    combo = itertools.product(demo,demo2)

#    for item in combo:
#         print item

check_combos(good_artifacts)
