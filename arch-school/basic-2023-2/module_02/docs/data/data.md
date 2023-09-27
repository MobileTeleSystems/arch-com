# Модель предметной области
<!-- Логическая модель, содержащая бизнес-сущности предметной области, атрибуты и связи между ними. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375782602

Используется диаграмма классов UML. Документация: https://plantuml.com/class-diagram 
-->

```plantuml
@startuml
' Логическая модель данных в варианте UML Class Diagram (альтернатива ER-диаграмме).
namespace ShoppingCart {

 class ShoppingCart
 {
  id : string
  createDate : datetime
  updateDate : datetime
  customer : Customer
  price : ShoppingCartPrice
  cartItems : CartItem[]
 }

 class ShoppingCartPrice
 {
  type : CartItemPrice
 }
 class CartItemPrice
 {
  type : CartItemPriceType
 }

 enum CartPriceType
 {
  total
  grandTotal
  offeringDiscount
  couponsDiscount
 }

 class CartItem
 {
  id : string
  quantity : int
  offering : Offering
  relationship : CartItemRelationShip[]
  price : CartItemPrice[]
  status : CartItemStatus
 }

  class Customer
 {
  id : string
 }
 
 class Offering
 {
  id : string
  isQuantifiable : boolean
  actionType : OfferingActionType
  validFor : ValidFor
 }
  
 class ProductSpecificationRef
 {
  id : string
 }
 
 ShoppingCart *-- "1..*" ShoppingCartPrice
 ShoppingCartPrice -- CartPriceType
 ShoppingCart *-- "*" CartItem
 CartItem *-- "*" CartItemPrice
 CartItemPrice -- CartPriceType
 CartItem *-- "1" Offering
 Offering *-- "1" ProductSpecificationRef
 Offering *-- "0..1" ProductConfiguration
 ShoppingCart *-- "1" Customer
}

namespace Ordering {
 ProductOrder *-- OrderItem
 OrderItem *-- Product
 Product *-- ProductSpecificationRef
 ProductOrder *-- Party
}

namespace ProductCatalog {
 ShoppingCart.ProductSpecificationRef ..> ProductSpecification : ref
 Ordering.ProductSpecificationRef ..> ProductSpecification : ref
}

namespace CX {
 ShoppingCart.Customer ..> Customer : ref
 Ordering.Party ..> Customer : ref
}
@enduml
```
