from service.report_parser.labs.thyrocare.entities import TestProfile

IRON_DEFICIENCY = TestProfile("IRON DEFICIENCY",
                              tests=["% TRANSFERRIN SATURATION",
                                     "TOTAL IRON BINDING CAPACITY",
                                     "IRON",
                                     "FERRITIN"])

LIVER = TestProfile("LIVER",
                    tests=["ALKALINE PHOSPHATASE",
                           "BILIRUBIN -DIRECT",
                           "BILIRUBIN - TOTAL",
                           "BILIRUBIN (INDIRECT)",
                           "GAMMA GLUTAMYL TRANSFERASE",
                           "SGOT / SGPT RATIO",
                           "ASPARTATE AMINOTRANSFERASE",
                           "ALANINE TRANSAMINASE",
                           "PROTEIN - TOTAL",
                           "ALBUMIN - SERUM",
                           "SERUM GLOBULIN",
                           "SERUM ALB/GLOBULIN RATIO"])

COMPLETE_HEMOGRAM = TestProfile("COMPLETE HEMOGRAM",
                                tests=["TOTAL LEUCOCYTES COUNT",
                                       "NEUTROPHILS",
                                       "LYMPHOCYTE PERCENTAGE",
                                       "MONOCYTES",
                                       "EOSINOPHILS",
                                       "BASOPHILS",
                                       "IMMATURE GRANULOCYTE PERCENTAGE",
                                       "NEUTROPHILS - ABSOLUTE COUNT",
                                       "LYMPHOCYTES - ABSOLUTE COUNT",
                                       "MONOCYTES - ABSOLUTE COUNT",
                                       "BASOPHILS - ABSOLUTE COUNT",
                                       "EOSINOPHILS - ABSOLUTE COUNT",
                                       "IMMATURE GRANULOCYTES",
                                       "TOTAL RBC",
                                       "NUCLEATED RED BLOOD CELLS",
                                       "NUCLEATED RED BLOOD CELLS %",
                                       "HEMOGLOBIN",
                                       "HEMATOCRIT",
                                       "MEAN CORPUSCULAR VOLUME",
                                       "MEAN CORPUSCULAR HEMOGLOBIN",
                                       "MEAN CORP.HEMO.CONC",
                                       "RED CELL DISTRIBUTION WIDTH - SD(RDW-SD)",
                                       "RED CELL DISTRIBUTION WIDTH (RDW-CV)",
                                       "PLATELET DISTRIBUTION WIDTH",
                                       "MEAN PLATELET VOLUME",
                                       "PLATELET COUNT",
                                       "PLATELET TO LARGE CELL RATIO",
                                       "PLATELETCRIT"])

DIABETES = TestProfile("DIABETES",
                       tests=["AVERAGE BLOOD GLUCOSE",
                              "HbA1c",
                              "BLOOD KETONE",
                              "FASTING BLOOD SUGAR",
                              "FRUCTOSAMINE",
                              "INSULIN",
                              "URINARY MICROALBUMIN"])

ARTHRITIS = TestProfile("ARTHRITIS",
                        tests=["ANTI CCP", "ANIT NUCLEAR ANTIBODIES"])

PANCREATIC = TestProfile("PANCREATIC",
                         tests=["AMYLASE", "LYPASE"])

CARDIAC_RISK_MARKERS = TestProfile("CARDIAC RISK MARKERS",
                                   tests=["APOLIPOPROTEIN - A1",
                                          "APOLIPOPROTEIN - B",
                                          "APO B / APO A1 RATIO",
                                          "HOMOCYSTEINE",
                                          "HIGH SENSITIVITY C-REACTIVE PROTEIN",
                                          "LIPOPROTEIN",
                                          "LP-PLA2"])

RENAL = TestProfile("RENAL",
                    tests=["BUN / Sr.CREATININE RATIO",
                           "BLOOD UREA NITROGEN",
                           "CALCIUM",
                           "CYSTATIN C",
                           "CREATININE - SERUM",
                           "URI. ALBUMIN/CREATININE RATIO",
                           "CREATININE - URINE",
                           "UREA / SR.CREATININE RATIO",
                           "UREA",
                           "URIC ACID",
                           "EST. GLOMERULAR FILTRATION RATE (eGFR)"])

TOXIC_ELEMENTS = TestProfile("TOXIC ELEMENTS",
                             tests=["SILVER",
                                    "ALUMINIUM",
                                    "ARSENIC",
                                    "BARIUM",
                                    "BERYLLIUM",
                                    "BISMUTH",
                                    "CADMIUM",
                                    "COBALT",
                                    "CHROMIUM",
                                    "CAESIUM",
                                    "MERCURY",
                                    "MANGANESE",
                                    "MOLYBDENUM",
                                    "NICKEL",
                                    "LEAD",
                                    "ANTIMONY",
                                    "SELENIUM",
                                    "TIN",
                                    "STRONTIUM",
                                    "THALLIUM",
                                    "URANIUM",
                                    "VANADIUM"])

ELECTROLYTES = TestProfile("ELECTROLYTES",
                           tests=["SODIUM", "CHLORIDE"])

LIPID = TestProfile("LIPID",
                    tests=["TOTAL CHOLESTEROL",
                           "HDL CHOLESTEROL - DIRECT",
                           "HDL / LDL RATIO",
                           "LDL CHOLESTEROL - DIRECT",
                           "TRIG / HDL RATIO",
                           "TRIGLYCERIDES",
                           "TC/ HDL CHOLESTEROL RATIO",
                           "LDL / HDL RATIO",
                           "VLDL CHOLESTEROL",
                           "NON-HDL CHOLESTEROL"])

METABOLIC = TestProfile("METABOLIC", tests=["MAGNESIUM"])

ELEMENTS = TestProfile("ELEMENTS", tests=["SERUM COPPER", "SERUM ZINC"])

URINOGRAM = TestProfile("URINOGRAM", tests=["SPECIFIC GRAVITY",
                                            "URINARY BILIRUBIN",
                                            "URINE BLOOD",
                                            "UROBILINOGEN",
                                            "URINARY GLUCOSE",
                                            "URINE KETONE",
                                            "URINARY LEUCOCYTES",
                                            "NITRITE",
                                            "PH",
                                            "URINARY PROTEIN"])

THYROID = TestProfile("THYROID", tests=["TOTAL TRIIODOTHYRONINE",
                                        "TOTAL THYROXINE",
                                        "THYROID STIMULATING HORMONE"])

HORMONE = TestProfile("HORMONE", tests=["TESTOSTERONE"])

VITAMINS = TestProfile("VITAMINS", tests=["VITAMIN A",
                                          "VITAMIN B-12",
                                          "VITAMIN B1/THIAMIN",
                                          "VITAMIN B2/RIBOFLAVIN",
                                          "VITAMIN B3/NICOTINIC ACID",
                                          "VITAMIN B5/PANTOTHENIC",
                                          "VITAMIN B6/PYRIDOXAL - 5 -PHOSPHATE",
                                          "VITAMIN B7/BIOTIN",
                                          "VITAMIN B9/FOLIC ACID",
                                          "25-OH VITAMIN D (TOTAL)",
                                          "VITAMIN E",
                                          "VITAMIN K"])


test_profiles = [IRON_DEFICIENCY,
                 LIVER,
                 COMPLETE_HEMOGRAM,
                 DIABETES,
                 ARTHRITIS,
                 PANCREATIC,
                 CARDIAC_RISK_MARKERS,
                 RENAL,
                 TOXIC_ELEMENTS,
                 ELECTROLYTES,
                 LIPID,
                 METABOLIC,
                 ELEMENTS,
                 URINOGRAM,
                 THYROID,
                 HORMONE,
                 VITAMINS]
