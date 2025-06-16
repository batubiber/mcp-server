"""
Versiyon bilgisi
"""
from dataclasses import dataclass

@dataclass
class VersiyonBilgisi:
    """
    Versiyon bilgisi
    """
    major_versiyon  : int = 0
    minor_versiyon  : int = 1
    build_versiyon  : int = 0
    product_id      : int = 0

    def __str__(self):
        return f"{self.major_versiyon}.{self.minor_versiyon}.{self.build_versiyon}.{self.product_id}"

    def __repr__(self):
        return self.__str__()

# VERSIYON GECMISI

####################################################################
# Versiyon : 1.0.0.0
# Yazanlar : Batuhan Biber
# Tarih    : 16.06.2025
#
# Gelismeler:
# - İnitial commit. 
# - Versiyon bilgisi eklendi.
#
####################################################################
