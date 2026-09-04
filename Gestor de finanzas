"""
PROYECTO DE SOFTWARE: GESTOR DE FINANZAS PERSONALES
Aplicación de 5 Patrones de Diseño en Python:
1. Singleton: Gestión centralizada del presupuesto y tipo de cambio.
2. Factory Method: Creación dinámica de transacciones (Ingreso / Gasto).
3. Strategy: Métodos de pago e impuestos (Efectivo / Tarjeta de Crédito).
4. Observer: Notificaciones de presupuesto y auditoría de saldo.
5. Decorator: Validación de transacciones y registro de logs.
"""

import time
from abc import ABC, abstractmethod

# ==========================================
# 1. PATRÓN SINGLETON (Creacional)
# ==========================================
class BilleteraCentral:
    """
    Garantiza que exista una única instancia que controle el saldo 
    global y la configuración presupuestaria de la aplicación.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BilleteraCentral, cls).__new__(cls)
            cls._instance.saldo = 0.0
            cls._instance.limite_diario = 100000.0  # Límite de gasto
            cls._instance.moneda = "COP"
        return cls._instance

    def actualizar_saldo(self, monto: float):
        self.saldo += monto

    def consultar_saldo(self) -> float:
        return self.saldo


# ==========================================
# 2. PATRÓN DECORATOR (Estructural)
# ==========================================
def validar_y_registrar(func):
    """
    Decorador que valida que los montos sean positivos y registra 
    la hora exacta en la que se realiza la transacción.
    """
    def wrapper(self, monto: float, descripcion: str, *args, **kwargs):
        if monto <= 0:
            print(f"  [ERROR - DECORATOR] Rechazado: El monto para '{descripcion}' debe ser mayor a 0.")
            return None
        
        hora_actual = time.strftime("%H:%M:%S")
        print(f"\n[DECORATOR {hora_actual}] Procesando transacción: '{descripcion}'")
        resultado = func(self, monto, descripcion, *args, **kwargs)
        return resultado
    return wrapper


# ==========================================
# 3. PATRÓN STRATEGY (Comportamental)
# ==========================================
class EstrategiaPago(ABC):
    """Interfaz para definir cómo se procesa y calcula el costo según el método de pago."""
    @abstractmethod
    def calcular_total(self, monto: float) -> float:
        pass

class PagoEfectivoStrategy(EstrategiaPago):
    def calcular_total(self, monto: float) -> float:
        print("  [STRATEGY] Pago en Efectivo: Sin comisiones adicionales.")
        return monto

class PagoTarjetaCreditoStrategy(EstrategiaPago):
    def calcular_total(self, monto: float) -> float:
        comision = monto * 0.05  # 5% de comisión / interés
        print(f"  [STRATEGY] Pago con Tarjeta de Crédito: Incluye 5% de comisión (+${comision:,.2f}).")
        return monto + comision


# ==========================================
# 4. PATRÓN FACTORY METHOD (Creacional)
# ==========================================
class Transaccion(ABC):
    """Clase base para transacciones."""
    def __init__(self, monto: float, descripcion: str):
        self.monto = monto
        self.descripcion = descripcion

    @abstractmethod
    def aplicar(self, billetera: BilleteraCentral):
        pass

class TransaccionIngreso(Transaccion):
    def aplicar(self, billetera: BilleteraCentral):
        billetera.actualizar_saldo(self.monto)
        print(f"  [FACTORY] + Ingreso registrado: ${self.monto:,.2f} por concepto de '{self.descripcion}'.")

class TransaccionGasto(Transaccion):
    def aplicar(self, billetera: BilleteraCentral):
        billetera.actualizar_saldo(-self.monto)
        print(f"  [FACTORY] - Gasto registrado: ${self.monto:,.2f} en '{self.descripcion}'.")

class TransaccionFactory:
    """Fábrica para instanciar tipos de transacciones sin acoplar la aplicación."""
    @staticmethod
    def crear_transaccion(tipo: str, monto: float, descripcion: str) -> Transaccion:
        tipo_normalizado = tipo.lower().strip()
        if tipo_normalizado == "ingreso":
            return TransaccionIngreso(monto, descripcion)
        elif tipo_normalizado == "gasto":
            return TransaccionGasto(monto, descripcion)
        else:
            raise ValueError(f"Tipo de transacción '{tipo}' no soportado.")


# ==========================================
# 5. PATRÓN OBSERVER (Comportamental)
# ==========================================
class ObservadorFinanciero(ABC):
    @abstractmethod
    def notificar(self, evento: str, saldo_actual: float):
        pass

class AlertaLimiteGastoObserver(ObservadorFinanciero):
    def notificar(self, evento: str, saldo_actual: float):
        if saldo_actual < 0:
            print(f"  [OBSERVER - ALERTA CRÍTICA] ¡Atención! Tu saldo quedó en números rojos: ${saldo_actual:,.2f}")

class AuditoriaGeneralObserver(ObservadorFinanciero):
    def notificar(self, evento: str, saldo_actual: float):
        print(f"  [OBSERVER - AUDITORÍA] Registro del evento '{evento}'. Saldo resultante: ${saldo_actual:,.2f}")

class GestorFinancieroSubject:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador: ObservadorFinanciero):
        self._observadores.append(observador)

    def notificar_observadores(self, evento: str, saldo_actual: float):
        for obs in self._observadores:
            obs.notificar(evento, saldo_actual)


# ==========================================
# PIPELINE / MOTOR PRINCIPAL DE LA APLICACIÓN
# ==========================================
class SistemaFinanzasPersonales(GestorFinancieroSubject):

    def __init__(self):
        super().__init__()
        self.billetera = BilleteraCentral()

    @validar_y_registrar
    def registrar_operacion(self, monto: float, descripcion: str, tipo_transaccion: str, estrategia_pago: EstrategiaPago = None):
        # 1. Ajustar el monto según la Estrategia de Pago (si aplica para gastos)
        monto_final = monto
        if estrategia_pago and tipo_transaccion.lower() == "gasto":
            monto_final = estrategia_pago.calcular_total(monto)

        # 2. Uso de Factory Method para crear el objeto de transacción
        transaccion = TransaccionFactory.crear_transaccion(tipo_transaccion, monto_final, descripcion)
        
        # 3. Aplicar transacción actualizando el Singleton (BilleteraCentral)
        transaccion.aplicar(self.billetera)

        # 4. Notificar mediante Observer la actualización
        saldo_actual = self.billetera.consultar_saldo()
        self.notificar_observadores(f"Operacion_{tipo_transaccion.upper()}", saldo_actual)


if __name__ == "__main__":
    print("==================================================")
    print(" GESTOR DE FINANZAS PERSONALES - PATRONES DE DISEÑO")
    print("==================================================")

    # Verificación del Singleton
    billetera_a = BilleteraCentral()
    billetera_b = BilleteraCentral()
    print(f"¿billetera_a y billetera_b corresponden al mismo estado global?: {billetera_a is billetera_b}")

    # Instanciar el sistema principal
    app = SistemaFinanzasPersonales()

    # Registrar observadores de alertas y auditoría
    app.agregar_observador(AuditoriaGeneralObserver())
    app.agregar_observador(AlertaLimiteGastoObserver())

    # 1. Registrar un Ingreso (Sueldo)
    app.registrar_operacion(1500000.0, "Pago de Nómina", "ingreso")

    # 2. Registrar un Gasto en Efectivo (Supermercado)
    app.registrar_operacion(200000.0, "Compra de víveres", "gasto", PagoEfectivoStrategy())

    # 3. Registrar un Gasto con Tarjeta de Crédito (Compra de electrodoméstico)
    app.registrar_operacion(1400000.0, "Televisor nuevo", "gasto", PagoTarjetaCreditoStrategy())

    # 4. Intentar una operación con monto inválido (Validación del Decorador)
    app.registrar_operacion(-50000.0, "Intento inválido", "gasto")