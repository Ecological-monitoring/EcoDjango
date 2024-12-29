

from django.db import models

class Pollutant(models.Model):
    name = models.CharField(max_length=100, help_text="Назва забруднюючої речовини")
    description = models.TextField(blank=True, null=True, help_text="Опис забруднюючої речовини")

    class Meta:
        db_table = 'eco_pollutant'  # Назва таблиці

    def __str__(self):
        return self.name

class PollutionRecord(models.Model):
    SUBSTANCE_CHOICES = [
        ('Оксид вуглецю', 'Оксид вуглецю'),
        ('Речовини у вигляді суспендованих твердих частинок', 'Речовини у вигляді суспендованих твердих частинок'),
        ('Діоксид азоту', 'Діоксид азоту'),
        ('Аміак', 'Аміак'),
        ('Сірки діоксид', 'Сірки діоксид'),
        ('Метан', 'Метан'),
    ]

    company = models.CharField(max_length=255)  # Назва компанії
    year = models.IntegerField()  # Рік
    value = models.FloatField()  # Значення викидів
    substance = models.CharField(max_length=255, choices=SUBSTANCE_CHOICES)  # Вибір речовини

    def __str__(self):
        return f"{self.company} ({self.year}) - {self.substance}"



class TaxRate(models.Model):
    pollutant = models.CharField(max_length=255, verbose_name="Забруднююча речовина")
    rate = models.FloatField(verbose_name="Ставка податку (грн за тонну)")

    def __str__(self):
        return f"{self.pollutant}: {self.rate} грн/тонна"





class TaxCalculation(models.Model):
    TAX_TYPES = [
        ('air', 'За викиди в атмосферне повітря'),
        ('water', 'За скиди у водні об’єкти'),
        ('waste', 'За розміщення відходів'),
        ('radioactive', 'За утворення радіоактивних відходів'),
        ('temporary', 'За тимчасове зберігання радіоактивних відходів')
    ]

    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, verbose_name="Забруднююча речовина")
    emission_volume = models.FloatField(verbose_name="Об'єм викидів (тонн)", blank=True, null=True)
    tax_rate = models.FloatField(verbose_name="Ставка податку (грн/тонна)", blank=True, null=True)
    tax_type = models.CharField(
        max_length=50,
        choices=TAX_TYPES,
        verbose_name="Тип податку",
        default='air'
    )

    tax_sum = models.FloatField(verbose_name="Сума податку (грн)", blank=True, null=True)
    calculation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата розрахунку")

    @staticmethod
    def calculate_air_tax(emissions):
        return sum(volume * rate for volume, rate in emissions)

    @staticmethod
    def calculate_water_tax(emissions, k_os=1):
        return sum(volume * rate * k_os for volume, rate in emissions)

    @staticmethod
    def calculate_waste_tax(emissions, k_t=1, k_o=1):
        return sum(rate * volume * k_t * k_o for volume, rate in emissions)

    @staticmethod
    def calculate_radioactive_waste_tax(On, N, coefficients):
        part1 = On * N
        part2 = coefficients['r_ns'] * coefficients['S1_ns'] * coefficients['V1_ns'] + \
                coefficients['r_v'] * coefficients['S1_v'] * coefficients['V1_v']
        part3 = (1 / 32) * (coefficients['r_ns'] * coefficients['S2_ns'] * coefficients['V2_ns'] + \
                            coefficients['r_v'] * coefficients['S2_v'] * coefficients['V2_v'])
        return part1 + part2 + part3

    @staticmethod
    def calculate_temporary_storage_tax(N, V, T):
        return N * V * T

    def save(self, *args, **kwargs):
        if self.tax_type == 'air' and self.emission_volume and self.tax_rate:
            self.tax_sum = self.calculate_air_tax([(self.emission_volume, self.tax_rate)])
        elif self.tax_type == 'water' and self.emission_volume and self.tax_rate:
            self.tax_sum = self.calculate_water_tax([(self.emission_volume, self.tax_rate)], k_os=1.5)
        elif self.tax_type == 'waste' and self.emission_volume and self.tax_rate:
            self.tax_sum = self.calculate_waste_tax([(self.emission_volume, self.tax_rate)], k_t=1.2, k_o=3)
        elif self.tax_type == 'radioactive':
            coefficients = {
                'r_ns': 0.8,
                'S1_ns': 500,
                'V1_ns': 10,
                'r_v': 1.2,
                'S1_v': 700,
                'V1_v': 5,
                'S2_ns': 300,
                'V2_ns': 20,
                'S2_v': 600,
                'V2_v': 8
            }
            self.tax_sum = self.calculate_radioactive_waste_tax(self.emission_volume, self.tax_rate, coefficients)
        elif self.tax_type == 'temporary':
            self.tax_sum = self.calculate_temporary_storage_tax(self.tax_rate, self.emission_volume, T=3)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.object_name} ({self.get_tax_type_display()})"



class EmissionRecord(models.Model):
    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, verbose_name="Забруднююча речовина")
    emission_volume = models.FloatField(verbose_name="Об'єм викидів (тонн)")
    date = models.DateField(verbose_name="Дата викиду")

    def __str__(self):
        return f"{self.object_name} - {self.pollutant.name} - {self.date}"

class RiskAssessment(models.Model):
    object_name = models.CharField(max_length=100, help_text="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, help_text="Забруднююча речовина")
    concentration = models.FloatField(help_text="Концентрація речовини, мг/м³")
    risk_level = models.CharField(max_length=100, blank=True, help_text="Рівень ризику")
    date = models.DateField(auto_now_add=True, help_text="Дата оцінки")


    def calculate_risk(self):
        """Обчислення ризику на основі методики"""
        # Додайте тут логіку оцінки ризику відповідно до методики
        if self.concentration > 1.0:  # Замініть 1.0 на ваші реальні порогові значення
            self.risk_level = "Високий"
        else:
            self.risk_level = "Низький"
        return self.risk_level

    def save(self, *args, **kwargs):
        self.calculate_risk()
        super().save(*args, **kwargs)



class DamageRecord(models.Model):
    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, verbose_name="Забруднююча речовина")
    emission_volume = models.FloatField(verbose_name="Обсяг викидів, скидів або розміщених відходів (М)", null=False, default=0.0)
    region_coefficient = models.FloatField(verbose_name="Регіональний коефіцієнт (К₃)", default=1.0)
    violation_characteristic = models.FloatField(verbose_name="Коефіцієнт характеру порушення (К₂)", default=1.0)
    year = models.IntegerField(verbose_name="Рік")
    damage_type = models.CharField(
        max_length=255,
        choices=[
            ('Air', 'Викиди в атмосферу'),
            ('Water', 'Скиди у водні об’єкти'),
            ('Soil', 'Забруднення ґрунту'),
        ],
        verbose_name="Тип завданої шкоди"
    )
    damage_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума збитків", null=True, blank=True)

    def calculate_damage(self):
        if not self.pollutant or not self.emission_volume:
            self.damage_amount = 0
            return

        base_damage = (
            self.emission_volume *
            self.pollutant.tax_rate *
            self.pollutant.hazard_coefficient *
            self.violation_characteristic *
            self.region_coefficient
        )

        if self.damage_type == 'Air':
            # Додаткові розрахунки для викидів в атмосферу (якщо потрібні)
            self.damage_amount = base_damage
        elif self.damage_type == 'Water':
            # Додаткові коефіцієнти для водних об’єктів
            water_coefficient = 1.5  # Приклад значення
            self.damage_amount = base_damage * water_coefficient
        elif self.damage_type == 'Soil':
            # Додаткові коефіцієнти для ґрунту
            soil_coefficient = 1.2  # Приклад значення
            self.damage_amount = base_damage * soil_coefficient
        else:
            self.damage_amount = base_damage

    def save(self, *args, **kwargs):
        self.calculate_damage()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.object_name} ({self.year})"

# Додаткова функція для розрахунку сумарного збитку
def calculate_total_damage():
    total_damage = 0
    records = DamageRecord.objects.all()
    for record in records:
        total_damage += float(record.damage_amount or 0)
    return total_damage

# Додаткова функція для розрахунку сумарного збитку
def calculate_total_damage():
    total_damage = 0
    records = DamageRecord.objects.all()
    for record in records:
        total_damage += float(record.damage_amount or 0)
    return total_damage



class EmergencyEvent(models.Model):
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=200)
    impact = models.TextField()

    def __str__(self):
        return self.name


class PollutantDetails(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва речовини")
    hazard_class = models.CharField(
        max_length=50,
        verbose_name="Клас небезпеки",
        choices=[
            ('I', 'І клас (надзвичайно небезпечні)'),
            ('II', 'ІІ клас (високонебезпечні)'),
            ('III', 'ІІІ клас (помірно небезпечні)'),
            ('IV', 'IV клас (малонебезпечні)')
        ],
        default='IV'  # Значення за замовчуванням
    )
    mpc = models.FloatField(verbose_name="ГДК (мг/м³)", null=True, blank=True)
    rfc = models.FloatField(verbose_name="RFC - безпечний рівень впливу речовини", null=True, blank=True)
    sf = models.FloatField(verbose_name="SF - фактор канцерогенного потенціалу", null=True, blank=True)
    specific_emissions = models.FloatField(verbose_name="Питомий показник викиду (qi)", null=True, blank=True)
    tax_rate = models.FloatField(verbose_name="Ставка податку (Сп)", null=True, blank=True)
    hazard_coefficient = models.FloatField(verbose_name="Коефіцієнт класу небезпеки (Кнеб)", null=True, blank=True)
    kn = models.FloatField(verbose_name="Коефіцієнт небезпечності (Кн)", null=True, blank=True)


    # Оцей метод прибрати, він не правильний, треба формулами
    def calculate_tax_rate(self):
        hazard_class_rates = {
            "I": 18413.24,  # грн/т
            "II": 4216.92,   # грн/т
            "III": 628.32,  # грн/т
            "IV": 145.50     # грн/т
        }
        return hazard_class_rates.get(self.hazard_class, 0)

    def calculate_kn(self):
        if self.mpc and self.specific_emissions:
            return self.mpc / self.specific_emissions
        return 0

    def calculate_hazard_coefficient(self):
        hazard_coefficients = {
            "I": 1.0,
            "II": 0.8,
            "III": 0.5,
            "IV": 0.2
        }
        return hazard_coefficients.get(self.hazard_class, 0)

    def calculate_pollution_tax(self):
        # Формула: Пвс = qi * Сп * Кнеб * Кн
        if self.specific_emissions and self.tax_rate and self.hazard_coefficient and self.kn:
            return self.specific_emissions * self.tax_rate * self.hazard_coefficient * self.kn
        return 0

    def save(self, *args, **kwargs):
        # Автоматично обчислюємо tax_rate, kn та hazard_coefficient перед збереженням
        self.tax_rate = self.calculate_tax_rate()
        self.kn = self.calculate_kn()
        self.hazard_coefficient = self.calculate_hazard_coefficient()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Додатковий функціонал для підрахунку загального податку для всіх речовин
def calculate_total_tax():
    total_tax = 0
    pollutants = PollutantDetails.objects.all()
    for pollutant in pollutants:
        total_tax += pollutant.calculate_pollution_tax()
    return total_tax



class EnvironmentalDamage(models.Model):
    TAX_TYPES = [
        ('land_pollution', 'Забруднення землі'),
        ('water_pollution', 'Забруднення води'),
        ('air_pollution', 'Забруднення повітря'),
        ('human_health', 'Втрати життя та здоров’я населення'),
        ('infrastructure_damage', 'Руйнування основних фондів'),
    ]

    object_name = models.CharField(max_length=255, verbose_name="Назва об'єкта")
    tax_type = models.CharField(max_length=50, choices=TAX_TYPES, verbose_name="Тип збитків")
    pollutant = models.ForeignKey('Pollutant', on_delete=models.CASCADE, verbose_name="Забруднююча речовина")
    report_year = models.IntegerField(verbose_name="Рік звітності")
    emission_volume = models.FloatField(verbose_name="Об'єм викидів (т/рік)", blank=True, null=True)
    mass_flow_rate = models.FloatField(verbose_name="Масова витрата (г/с)", blank=True, null=True)
    concentration = models.FloatField(verbose_name="Концентрація сполук у повітрі (мг/м³)", blank=True, null=True)
    area = models.FloatField(verbose_name="Площа впливу (м²)", blank=True, null=True)
    human_losses = models.FloatField(verbose_name="Втрати трудових ресурсів", blank=True, null=True)
    infrastructure_losses = models.FloatField(verbose_name="Руйнування основних фондів", blank=True, null=True)
    damage_sum = models.FloatField(verbose_name="Сума збитків (грн)", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.tax_type == 'land_pollution':
            self.damage_sum = self.calculate_land_pollution_damage()
        elif self.tax_type == 'water_pollution':
            self.damage_sum = self.calculate_water_pollution_damage()
        elif self.tax_type == 'air_pollution':
            self.damage_sum = self.calculate_air_pollution_damage()
        elif self.tax_type == 'human_health':
            self.damage_sum = self.calculate_human_health_damage()
        elif self.tax_type == 'infrastructure_damage':
            self.damage_sum = self.calculate_infrastructure_damage()

        super().save(*args, **kwargs)

    def calculate_land_pollution_damage(self):
        # Формула для забруднення землі
        Yn = 1.0  # коефіцієнт екологічної небезпеки
        n = 1.0   # кількість забруднювачів
        M = self.emission_volume or 0
        L = 1.0   # відносна природна захищеність
        return Yn * n * M * L

    def calculate_water_pollution_damage(self):
        # Формула для водних ресурсів
        S = self.area or 0
        H = 1.0   # глибина впливу
        P = self.mass_flow_rate or 0
        R = 1.0   # коефіцієнт ризику
        V = 1.0   # швидкість розповсюдження
        K1 = 1.0  # коефіцієнт впливу
        K2 = 1.0  # коефіцієнт відновлення
        return (S * H * P * (R / V) * K1 * (10 ** -6)) / (100 * K2)

    def calculate_air_pollution_damage(self):
        # Формула для забруднення повітря
        M = self.mass_flow_rate or 0
        C = self.concentration or 0
        return M * C

    def calculate_human_health_damage(self):
        # Формула для втрат життя та здоров'я
        S_vtrr = 100000  # втрати трудових ресурсів
        S_vdp = 50000    # виплати на поховання
        S_vvtg = 200000  # виплати пенсій
        return S_vtrr + S_vdp + S_vvtg

    def calculate_infrastructure_damage(self):
        # Формула для руйнування інфраструктури
        Fv = 500000  # основні фонди
        Fg = 300000  # будівлі
        Pr = 200000  # обладнання
        Prs = 100000 # склади
        Sn = 150000  # техніка
        Mdg = 250000 # матеріали
        return Fv + Fg + Pr + Prs + Sn + Mdg

    def __str__(self):
        return f"{self.object_name} ({self.get_tax_type_display()})"
