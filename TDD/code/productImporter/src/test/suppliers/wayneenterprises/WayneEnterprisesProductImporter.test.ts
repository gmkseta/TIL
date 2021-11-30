import { Product } from "../../../main/Product";
import { WayneEnterprisesProduct } from "../../../main/wayneenterprises/WayneEnterprisesProduct";
import { WayneEnterprisesProductImporter } from "../../../main/wayneenterprises/WayneEnterprisesProductImporter";
import { WayneEnterprisesProductSourceStub } from "./WayneEnterprisesProductSourceStub";

// public class WayneEnterprisesProductImporter_specs {
describe('WayneEnterprisesProductImporter_specs ', () => {
    const source = new WayneEnterprisesProduct();

    test('sut_projects_all_products', () => {
        let stub = new WayneEnterprisesProductSourceStub(source);
        let sut = new WayneEnterprisesProductImporter(stub);
        let actual: Iterable<Product>  = sut.fetchProducts();

        expect(Array.from(actual).length).toBe(source.length);
    });

})
    

//     @ParameterizedTest
//     @DomainArgumentsSource
//     void sut_correctly_sets_supplier_name(WayneEnterprisesProduct[] source) {
//         var stub = new WayneEnterprisesProductSourceStub(source);
//         var sut = new WayneEnterprisesProductImporter(stub);

//         Iterable<Product> actual = sut.fetchProducts();

//         assertThat(actual).allMatch(x -> x.getSupplierName().equals("WAYNE"));
//     }

//     @ParameterizedTest
//     @DomainArgumentsSource
//     void sut_correctly_projects_source_properties(WayneEnterprisesProduct source) {
//         var stub = new WayneEnterprisesProductSourceStub(source);
//         var sut = new WayneEnterprisesProductImporter(stub);

//         List<Product> products = new ArrayList<Product>();
//         sut.fetchProducts().forEach(products::add);
//         Product actual = products.get(0);

//         assertThat(actual.getProductCode()).isEqualTo(source.getId());
//         assertThat(actual.getProductName()).isEqualTo(source.getTitle());
//         assertThat(actual.getPricing().getListPrice()).isEqualByComparingTo(Integer.toString(source.getListPrice()));
//         assertThat(actual.getPricing().getDiscount())
//                 .isEqualByComparingTo(Integer.toString(source.getListPrice() - source.getSellingPrice()));
//     }
// }
