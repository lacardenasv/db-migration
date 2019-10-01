#select_all_query = lambda model_ref : SELECT {}format(*model_attr)
insert_sql = lambda table, attr: 'INSERT INTO {0} {1} VALUES %s'.format(table, attr)
drop_table_sql = lambda table_name: 'DROP TABLE IF EXISTS {} CASCADE'.format(table_name)
count_rows_sql = lambda table_name: 'SELECT COUNT(*) FROM {}'.format(table_name)
select_table_postgres = lambda table_name: 'SELECT * FROM {};'.format(table_name)

MODEL_ATTRS = {
    # main app
    'TESTIMONIAL': '("content", "position", "company_name", "replica", "client_id", "user", "first_name", "last_name", "show", "date_added", "last_modified")',
    'CALL_ZINC_LOG': '("file_path", "file_name", "file_type", "month_added", "year_added", "date_added", "last_modified")',
    'CONTACT_REASON': '("code", "value", "date_added")',
    'DISCOVER_SETTINGS': '("welcome_modal_status", "client_id", "replica", "date")',
    'PARTNER': '("code", "name", "has_marketplace", "has_walmart", "has_taobao", "has_aliexpress", "last_modified")',
    # marketplace app
    'CART_PRODUCT': '("asin", "store", "name", "picture", "original_price", "shipping_price", "shipping_method", "total_price", "trm", "ultrabox_fee_shipping", "ultrabox_fee_tax", "date_added", "weight", "height", "length", "width", "package_height", "package_length", "package_width", "size_unit", "discount", "quantity", "total_response_ws", "cupon", "features", "details")',
    'CHECKOUT_DATA': '("cc_name", "cc_number", "cc_ccv", "cc_date", "cc_type", "billing_name", "billing_surname", "billing_address", "billing_zip", "billing_city", "billing_state", "billing_country" , "billing_phone", "amazon_email", "amazon_password", "date_added", "last_modified")',
    'CUSTOMER': '("email", "password", "client_id", "ally", "name", "surname", "country", "identification_number", "client_type", "is_colsubsidio", "date_added", "last_modified")',
    'HIGHLIGHTED_PRODUCT': '("store", "date", "info", "replica", "image", "asin", "title", "original_price", "currency_code", "type")',
    'MEMBERSHIP': '("email", "state")',
    'AMAZON_MENU_HOME': '("nombre", "index", "pertenece_id")',
    'ORDER': '("id", "trm", "ip", "date_added", "last_modified", "process", "payu_active", "prealerta", "customer_id", "payment_data_id")',
    'ORDER_PACKAGE': '("package_id", "zinc_registry_id")',
    'P2P_SETTINGS': '("id", "p2p_trankey", "p2p_loginkey", "environment", "replica")',
    'P2P_TRANSACCTION': '("id", "status", "status_p2p", "order_id", "p2p_date", "p2p_internal_ref", "p2p_authorization_code", "replica", "date_added", "last_modified", "total")',
    'PAYMENT_DATA': '("cc_payu_token", "payment_method", "cc_type", "billing_name", "billing_lastname", "billing_address", "billing_zip", "billing_city", "billing_state", "billing_country", "billing_phone", "date_added", "last_modified")',
    'PAYU_TRANSACTION': '("id", "status", "status_payu", "order_id", "date_added", "last_modified", "total")',
    'PRODUCT': '("transaction_id", "asin", "name", "picture", "weight", "height", "length", "width", "package_height", "package_length", "package_width", "size_unit", "price", "quantity", "discount", "cupon", "original_price", "shipping_price", "shipping_method", "features")',
    'RETAILER_CREDENTIALS': '("email", "password", "date_added", "last_modified")',
    'TOKEN_EBAY': '("token", "token_expire", "refresh_token", "refresh_token_expire")',
    'TRANSACTION': '("transaction_id", "order_id", "status", "ultrabox_fee", "error_code", "store", "total_value", "retailer_credentials_id", "date_added", "last_modified", "adicional_data", "zinc_precio")',
    'ZINC_CART_ITEM': '("zinc_registry_id", "asin", "weight", "height", "length", "width", "package_height", "package_length", "package_width", "size_unit", "original_price", "name", "quantity")',
    'ZINC_TEMP_REQUEST_ID': '("request_id", "error_code", "ip_address", "payu_transaction_id", "checkout_data_id", "customer_data_id", "shipping", "subtotal", "trm", "tax", "ultrabox_fee_shipping", "ultrabox_fee_tax", "total", "date_added", "last_modified", "cart_id", "amazon_satate", "payu_state", "error_zinc", "paso_payu")',
    'CART': '("creation_date", "checked_out", "client_id", "abandoned", "last_item_added")',
    'ITEM': '("cart_id", "quantity", "unit_price", "content_type_id", "object_id")',
    'VISITED_PRODUCT': '( "asin", "store", "name", "picture", "weight", "height", "length", "width", "weight_unit", "package_height", "package_length", "package_width", "size_unit", "total_price", "total_unit_price", "quantity", "discount", "cupon", "original_price", "date_added", "last_modified")',

    #  IMPORTANT: This model is dor crawler data migration about amazon products this model is at marketplace app
    'CRAWLER_PRODUCT': '("title" ,"product_url", "listing_url" ,"price" ,"primary_img" ,"crawl_time" ,"category_code", "category", "features", "asin", "dimensions", "weight", "shipping_weight", "package_dimensions", "package_weight")',
}


ALTER_AND_CREATE_INDEX_BY_APP = {
    'CART': {
        'NEXT_OPERATIONS': (
            'ALTER TABLE "cart_item" ADD CONSTRAINT "cart_item_cart_id_157ecf5f_fk_cart_cart_id" FOREIGN KEY ("cart_id") REFERENCES "cart_cart" ("id") DEFERRABLE INITIALLY DEFERRED',
            'ALTER TABLE "cart_item" ADD CONSTRAINT "cart_item_content_type_id_5737916f_fk_django_content_type_id" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "cart_item_c44d83f7" ON "cart_item" ("cart_id")',
            'CREATE INDEX "cart_item_417f1b1c" ON "cart_item" ("content_type_id")',
        )
    },
    'MARKETPLACE': {
        'NEXT_OPERATIONS': (
            # Add field zinc_registry to zinccartitem
            'ALTER TABLE "marketplace_zinccartitem" ADD COLUMN "zinc_registry_id" integer NOT NULL',
            'ALTER TABLE "marketplace_zinccartitem" ALTER COLUMN "zinc_registry_id" DROP DEFAULT',
            # Add field transaction to product
            'ALTER TABLE "marketplace_product" ADD COLUMN "transaction_id" integer NOT NULL',
            'ALTER TABLE "marketplace_product" ALTER COLUMN "transaction_id" DROP DEFAULT',
            # Add field zinc_registry to orderpackage
            'ALTER TABLE "marketplace_orderpackage" ADD COLUMN "zinc_registry_id" integer NOT NULL',
            'ALTER TABLE "marketplace_orderpackage" ALTER COLUMN "zinc_registry_id" DROP DEFAULT',
            # Add field payment_data to order
            'ALTER TABLE "marketplace_order" ADD COLUMN "payment_data_id" integer NULL',
            'ALTER TABLE "marketplace_order" ALTER COLUMN "payment_data_id" DROP DEFAULT',
            'ALTER TABLE "marketplace_menuamazonmphome" ADD CONSTRAINT "market_pertenece_id_07ca2a16_fk_marketplace_menuamazonmphome_id" FOREIGN KEY ("pertenece_id") REFERENCES "marketplace_menuamazonmphome" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_menuamazonmphome_ca685d7e" ON "marketplace_menuamazonmphome" ("pertenece_id")',
            'ALTER TABLE "marketplace_order" ADD CONSTRAINT "marketplace_ord_customer_id_37cd991e_fk_marketplace_customer_id" FOREIGN KEY ("customer_id") REFERENCES "marketplace_customer" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_order_cb24373b" ON "marketplace_order" ("customer_id")',
            'CREATE INDEX "marketplace_order_id_db2255f6_like" ON "marketplace_order" ("id" varchar_pattern_ops)',
            'CREATE INDEX "marketplace_p2psettings_id_af7c2d57_like" ON "marketplace_p2psettings" ("id" varchar_pattern_ops)',
            'ALTER TABLE "marketplace_p2ptransaction" ADD CONSTRAINT "marketplace_p2ptransa_order_id_c638a8d3_fk_marketplace_order_id" FOREIGN KEY ("order_id") REFERENCES "marketplace_order" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_p2ptransaction_69dfcb07" ON "marketplace_p2ptransaction" ("order_id")',
            'CREATE INDEX "marketplace_p2ptransaction_id_c349aecc_like" ON "marketplace_p2ptransaction" ("id" varchar_pattern_ops)',
            'CREATE INDEX "marketplace_p2ptransaction_order_id_c638a8d3_like" ON "marketplace_p2ptransaction" ("order_id" varchar_pattern_ops)',
            'ALTER TABLE "marketplace_payutransaction" ADD CONSTRAINT "marketplace_payutrans_order_id_05f33c9e_fk_marketplace_order_id" FOREIGN KEY ("order_id") REFERENCES "marketplace_order" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_payutransaction_69dfcb07" ON "marketplace_payutransaction" ("order_id")',
            'CREATE INDEX "marketplace_payutransaction_id_589afdf5_like" ON "marketplace_payutransaction" ("id" varchar_pattern_ops)',
            'CREATE INDEX "marketplace_payutransaction_order_id_05f33c9e_like" ON "marketplace_payutransaction" ("order_id" varchar_pattern_ops)',
            'ALTER TABLE "marketplace_transaction" ADD CONSTRAINT "marketplace_transacti_order_id_5cd9e377_fk_marketplace_order_id" FOREIGN KEY ("order_id") REFERENCES "marketplace_order" ("id") DEFERRABLE INITIALLY DEFERRED',
            'ALTER TABLE "marketplace_transaction" ADD CONSTRAINT "e1ff55e0ab9fe284a2b5f09edabb6d2d" FOREIGN KEY ("retailer_credentials_id") REFERENCES "marketplace_retailercredentials" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_transaction_69dfcb07" ON "marketplace_transaction" ("order_id")',
            'CREATE INDEX "marketplace_transaction_d5231f9d" ON "marketplace_transaction" ("retailer_credentials_id")',
            'CREATE INDEX "marketplace_transaction_order_id_5cd9e377_like" ON "marketplace_transaction" ("order_id" varchar_pattern_ops)',
            'ALTER TABLE "marketplace_zinctemprequestid" ADD CONSTRAINT "marketplace_zinctemprequestid_cart_id_99d1254a_fk_cart_cart_id" FOREIGN KEY ("cart_id") REFERENCES "cart_cart" ("id") DEFERRABLE INITIALLY DEFERRED',
            'ALTER TABLE "marketplace_zinctemprequestid" ADD CONSTRAINT "market_checkout_data_id_45652fe1_fk_marketplace_checkoutdata_id" FOREIGN KEY ("checkout_data_id") REFERENCES "marketplace_checkoutdata" ("id") DEFERRABLE INITIALLY DEFERRED',
            'ALTER TABLE "marketplace_zinctemprequestid" ADD CONSTRAINT "marketplac_customer_data_id_14d68027_fk_marketplace_customer_id" FOREIGN KEY ("customer_data_id") REFERENCES "marketplace_customer" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_zinctemprequestid_c44d83f7" ON "marketplace_zinctemprequestid" ("cart_id")',
            'CREATE INDEX "marketplace_zinctemprequestid_82a81acd" ON "marketplace_zinctemprequestid" ("checkout_data_id")',
            'CREATE INDEX "marketplace_zinctemprequestid_19381865" ON "marketplace_zinctemprequestid" ("customer_data_id")',
            'CREATE INDEX "marketplace_zinccartitem_76415b32" ON "marketplace_zinccartitem" ("zinc_registry_id")',
            'ALTER TABLE "marketplace_zinccartitem" ADD CONSTRAINT "m_zinc_registry_id_4c6fcb74_fk_marketplace_zinctemprequestid_id" FOREIGN KEY ("zinc_registry_id") REFERENCES "marketplace_zinctemprequestid" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_product_f847de52" ON "marketplace_product" ("transaction_id")',
            'ALTER TABLE "marketplace_product" ADD CONSTRAINT "marketpla_transaction_id_daf0a0b6_fk_marketplace_transaction_id" FOREIGN KEY ("transaction_id") REFERENCES "marketplace_transaction" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_orderpackage_76415b32" ON "marketplace_orderpackage" ("zinc_registry_id")',
            'ALTER TABLE "marketplace_orderpackage" ADD CONSTRAINT "m_zinc_registry_id_ecde0404_fk_marketplace_zinctemprequestid_id" FOREIGN KEY ("zinc_registry_id") REFERENCES "marketplace_zinctemprequestid" ("id") DEFERRABLE INITIALLY DEFERRED',
            'CREATE INDEX "marketplace_order_9caf2f0e" ON "marketplace_order" ("payment_data_id")',
            'ALTER TABLE "marketplace_order" ADD CONSTRAINT "marketpl_payment_data_id_d1594a69_fk_marketplace_paymentdata_id" FOREIGN KEY ("payment_data_id") REFERENCES "marketplace_paymentdata" ("id") DEFERRABLE INITIALLY DEFERRED',
        )
    }
}

INSERT_BY_ORDER = (
    'TESTIMONIAL',
    'CALL_ZINC_LOG',
    'CONTACT_REASON',
    'DISCOVER_SETTINGS',
    'PARTNER',
    'CART_PRODUCT',
    'CHECKOUT_DATA',
    'CUSTOMER',
    #'HIGHLIGHTED_PRODUCT',
    'MEMBERSHIP',
    'AMAZON_MENU_HOME',
    'PAYMENT_DATA',
    'ORDER',
    'ZINC_TEMP_REQUEST_ID',
    'ORDER_PACKAGE',
    'P2P_SETTINGS',
    'P2P_TRANSACCTION',
    'PAYU_TRANSACTION',
    'RETAILER_CREDENTIALS',
    'TOKEN_EBAY',
    'TRANSACTION',
    'PRODUCT',
    'ZINC_CART_ITEM',
    'VISITED_PRODUCT'
)

















OPERATIONS_BY_MODEL = {

    #  IMPORTANT: This model is dor crawler data migration about amazon products this model is at marketplace app
    'CRAWLER_PRODUCT': {
        'CREATE': """CREATE TABLE marketplace_crawledamazonproduct (
            id          serial PRIMARY KEY,
            title       varchar(2056),
            product_url         varchar(2056),
            listing_url varchar(2056),
            price       varchar(128),
            primary_img varchar(2056),
            crawl_time timestamp,
            category_code integer,
            asin varchar(256) null,
            category varchar(256),
            features text[] null default '{}',
            dimensions jsonb DEFAULT '{}' NULL, 
            weight double precision NULL,
            shipping_weight double precision NULL,
            package_dimensions jsonb DEFAULT '{}' NULL,
            package_weight double precision NULL
        );""",
        'SELECT': 'SELECT title, product_url, listing_url, price, primary_img, crawl_time, category_code, category, features, asin, dimensions, weight, shipping_weight, package_dimensions, package_weight FROM marketplace_crawledamazonproduct;',
        'INSERT': insert_sql('marketplace_crawledamazonproduct', MODEL_ATTRS["CRAWLER_PRODUCT"]),
        'DELETE': drop_table_sql('marketplace_crawledamazonproduct'),
        'COUNT': count_rows_sql('marketplace_crawledamazonproduct')
     },
}
