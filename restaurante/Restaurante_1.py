import time
from abc import ABC, abstractmethod

# ==================================================
# 1. PATRÓN SINGLETON (Creacional)
# ==================================================
class CajaRestaurante:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.total_ventas = 0.0
            cls._instancia.observadores = []
        return cls._instancia

    def registrar_observador(self, observador):
        self.observadores.append(observador)

    def notificar_observadores(self, item_nombre, total_pedido):
        for obs in self.observadores:
            obs.actualizar(item_nombre, total_pedido, self.total_ventas)

    def registrar_venta(self, item_nombre, monto):
        self.total_ventas += monto
        self.notificar_observadores(item_nombre, monto)
        return self.total_ventas


# ==================================================
# 2. PATRÓN DECORATOR (Estructural)
# ==================================================
def validar_y_registrar_pedido(func):
    def wrapper(self, cantidad: int, *args, **kwargs):
        if cantidad <= 0:
            print(f"  [ERROR - DECORATOR] Rechazado: La cantidad de '{self.nombre}' debe ser mayor a 0.")
            return None
        
        hora_actual = time.strftime("%H:%M:%S")
        print(f"\n[DECORATOR {hora_actual}] Procesando orden: {cantidad}x '{self.nombre}'")
        return func(self, cantidad, *args, **kwargs)
    return wrapper


# ==================================================
# 3. PATRÓN STRATEGY (Comportamiento)
# ==================================================
class EstrategiaEntrega(ABC):
    @abstractmethod
    def calcular_costo_envio(self, subtotal: float) -> float:
        pass

class EnMesaStrategy(EstrategiaEntrega):
    def calcular_costo_envio(self, subtotal: float) -> float:
        print("  [STRATEGY] Servicio en Mesa: Sin costo adicional de envío.")
        return 0.0

class DomicilioStrategy(EstrategiaEntrega):
    def __init__(self, tarifa_domicilio=5000.0):
        self.tarifa = tarifa_domicilio

    def calcular_costo_envio(self, subtotal: float) -> float:
        print(f"  [STRATEGY] Envió a Domicilio: Recargo de servicio (+${self.tarifa:,.2f}).")
        return self.tarifa


# ==================================================
# 4. PATRÓN FACTORY METHOD (Creacional)
# ==================================================
class Producto(ABC):
    @abstractmethod
    def preparar_orden(self, cantidad: int):
        pass

class PlatoComida(Producto):
    def __init__(self, nombre: str, precio_base: float, estrategia_entrega=None):
        self.nombre = nombre
        self.precio_base = precio_base
        self.estrategia_entrega = estrategia_entrega
        self.caja = CajaRestaurante()

    @validar_y_registrar_pedido
    def preparar_orden(self, cantidad: int):
        subtotal = self.precio_base * cantidad
        recargo_envio = 0.0
        if self.estrategia_entrega:
            recargo_envio = self.estrategia_entrega.calcular_costo_envio(subtotal)
        
        total_final = subtotal + recargo_envio
        self.caja.registrar_venta(self.nombre, total_final)
        print(f"  [FACTORY] + Platillo listo: {cantidad}x '{self.nombre}' | Total: ${total_final:,.2f}")

class Bebida(Producto):
    def __init__(self, nombre: str, precio_base: float, estrategia_entrega=None):
        self.nombre = nombre
        self.precio_base = precio_base
        self.estrategia_entrega = estrategia_entrega
        self.caja = CajaRestaurante()

    @validar_y_registrar_pedido
    def preparar_orden(self, cantidad: int):
        subtotal = self.precio_base * cantidad
        recargo_envio = 0.0
        if self.estrategia_entrega:
            recargo_envio = self.estrategia_entrega.calcular_costo_envio(subtotal)
            
        total_final = subtotal + recargo_envio
        self.caja.registrar_venta(self.nombre, total_final)
        print(f"  [FACTORY] + Bebida servida: {cantidad}x '{self.nombre}' | Total: ${total_final:,.2f}")

class PedidoFactory:
    @staticmethod
    def crear_producto(tipo: str, nombre: str, precio_base: float, estrategia_entrega=None):
        tipo_lower = tipo.lower()
        if tipo_lower == "comida":
            return PlatoComida(nombre, precio_base, estrategia_entrega)
        elif tipo_lower == "bebida":
            return Bebida(nombre, precio_base, estrategia_entrega)
        else:
            raise ValueError(f"Tipo de producto '{tipo}' no soportado.")


# ==================================================
# 5. PATRÓN OBSERVER (Comportamiento)
# ==================================================
class ObservadorRestaurante(ABC):
    @abstractmethod
    def actualizar(self, item_nombre: str, total_pedido: float, total_caja: float):
        pass

class PantallaCocina(ObservadorRestaurante):
    def actualizar(self, item_nombre: str, total_pedido: float, total_caja: float):
        print(f"  [OBSERVER - COCINA] Orden recibida en cocina: Preparing '{item_nombre}'.")

class MonitorCaja(ObservadorRestaurante):
    def actualizar(self, item_nombre: str, total_pedido: float, total_caja: float):
        print(f"  [OBSERVER - CAJA] Venta cobrada: +${total_pedido:,.2f} | Acumulado del día: ${total_caja:,.2f}")


# ==================================================
# PRUEBA Y SIMULACIÓN
# ==================================================
if __name__ == "__main__":
    caja_a = CajaRestaurante()
    caja_b = CajaRestaurante()

    print("==================================================")
    print(" SISTEMA DE PEDIDOS RESTAURANTE - PATRONES DE DISEÑO")
    print("==================================================")
    print("¿caja_a y caja_b apuntan a la misma CajaCentral?:", caja_a is caja_b)

    # Registrar observadores
    caja_a.registrar_observador(PantallaCocina())
    caja_a.registrar_observador(MonitorCaja())

    # Pedido 1: Comida para comer en el lugar
    p1 = PedidoFactory.crear_producto("comida", "Hamburguesa Doble", 25000, EnMesaStrategy())
    p1.preparar_orden(2)

    # Pedido 2: Bebida a Domicilio (aplica Strategy con recargo)
    p2 = PedidoFactory.crear_producto("bebida", "Jugo Natural", 8000, DomicilioStrategy())
    p2.preparar_orden(3)

    # Pedido 3: Intento inválido (probando validación del Decorator)
    p3 = PedidoFactory.crear_producto("comida", "Pizza Familiar", 45000)
    p3.preparar_orden(0)