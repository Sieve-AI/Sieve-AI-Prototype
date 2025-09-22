data_schema_manager = {
    "prompt": "Utilizando el siguiente esquema JSON, extrae y estructura la información del texto proporcionado. El objetivo es mantener la correlación de los datos en 'filas' como en un dataframe. Para cada propiedad en el esquema, el resultado debe ser un array. Identifica los grupos de datos relacionados y asigna cada valor a la posición correspondiente en el array. Si para una 'fila' no existe un dato para una propiedad, rellena su posición en el array con el valor 'n/a' para mantener la alineación con las demás propiedades. Los campos `description` y `class_data` proporcionan contexto sobre el tipo de dato a extraer. Asegúrese de que los valores extraídos coincidan con el `type` y `format` especificados. Al finalizar el procesamiento, la salida JSON debe incluir únicamente las propiedades que contengan valores extraídos, omitiendo aquellas que queden con un valor `null`. Adicionalmente, si la información extraída es suficiente para generar un reporte de uno de los tipos definidos, incluya un objeto `generated_report` en la raíz de la salida JSON. Este objeto debe contener `report_type` (el tipo de reporte generado), `variables_and_standards` (las variables y estándares utilizados), y una sección de `findings` con las observaciones relevantes y los puntos clave de la información. Las opciones de reportes disponibles se encuentran en `report_types`, con las opciones clasificadas dentro de `related_reports` y los datos para alimentarlos se extraen de las clases de `data_distributions` asociadas a cada tipo de reporte. Esto permite una mejor gestión de los datos para la obtención de respuestas. La salida final debe ser un solo objeto JSON que se ajuste a este esquema.",
    "data_distributions": {
        "description": "Clasificación de las propiedades del esquema en cuatro categorías principales de distribución de datos.",
        "label_data": [
            "identifiers",
            "classification_code",
            "text_string",
            "mixed",
            "people_and_places_id",
            "free_text"
        ],
        "measure_data": [
            "cientific_measurement",
            "proportion_and_average",
            "coordenates",
            "date_time_event",
            "sensor_and_time_series",
            "calendar"
        ],
        "transaction_data": [
            "counted_values",
            "monetary_values"
        ],
        "condition_data": [
            "categorical_values",
            "limited_and_concrete",
            "rating_and_ranks",
            "columns_from_conditions",
            "record_states",
            "logical_comparison"
        ]
    },
    "report_types": {
        "description": "Clasificación de tipos de informes según las distribuciones de datos que utilizan.",
        "results_report": {
            "data_distributions": [
                "transaction_data",
                "label_data"
            ],
            "related_reports": [
                "Executive Summary",
                "Project or Event Context",
                "Results Achieved",
                "Key Decision Analysis",
                "Lessons Learned",
                "Recommendations for the Future"
            ]
        },
        "bias_report": {
            "data_distributions": [
                "label_data",
                "condition_data"
            ],
            "related_reports": [
                "Confirmation Bias",
                "Hindsight Bias",
                "Anchoring Bias",
                "Availability Bias",
                "Halo Effect",
                "Social Desirability Bias",
                "Selection Bias"
            ]
        },
        "control_report": {
            "data_distributions": [
                "condition_data",
                "measure_data"
            ],
            "related_reports": [
                "Data Auditing and Validation Report",
                "Classification and Diagnostic Report",
                "Control Variable Monitoring Report"
            ]
        },
        "prediction_report": {
            "data_distributions": [
                "measure_data",
                "transaction_data"
            ],
            "related_reports": [
                "Trend Analysis Report",
                "Scenario Planning Report",
                "Projection Forecast Report",
                "Risk and Opportunity Analysis Report"
            ]
        },
        "distribution_report": {
            "data_distributions": [
                "label_data",
                "measure_data"
            ],
            "related_reports": [
                "Frequency Analysis Report",
                "Descriptive Analysis Report",
                "Root Cause Analysis Report",
                "Correlation Analysis Report"
            ]
        },
        "management_report": {
            "data_distributions": [
                "transaction_data",
                "condition_data"
            ],
            "related_reports": [
                "Trend Analysis Report",
                "Scenario Planning Report",
                "Projection Forecast Report",
                "Risk and Opportunity Analysis Report"
            ]
        }
    },
    "report_schemas": {
        "description": "Asociación de cada tipo de informe con un esquema de análisis (Hindsight, Insight, Foresight).",
        "results_report": "Hindsight",
        "bias_report": "Insight",
        "control_report": "Insight",
        "prediction_report": "Foresight",
        "distribution_report": "Insight",
        "management_report": "Foresight"
    },
    "type": "object",
    "description": "Esquema unificado y estructurado para procesar archivos de texto y extraer información relevante para un agente de Vertex AI.",
    "properties": {
        "identifiers_and_codes": {
            "type": "object",
            "description": "Identificadores únicos y códigos de clasificación.",
            "properties": {
                "client_id": {
                    "type": "array",
                    "description": "Identificador numérico único para un cliente.",
                    "items": { "type": "integer" },
                    "class_data": "identifiers"
                },
                "product_id": {
                    "type": "array",
                    "description": "Identificador numérico único para un producto.",
                    "items": { "type": "integer" },
                    "class_data": "identifiers"
                },
                "order_number": {
                    "type": "array",
                    "description": "Identificador numérico único para un pedido de cliente.",
                    "items": { "type": "integer" },
                    "class_data": "identifiers"
                },
                "employee_number": {
                    "type": "array",
                    "description": "Identificador numérico único para un empleado.",
                    "items": { "type": "integer" },
                    "class_data": "identifiers"
                },
                "postal_code": {
                    "type": "array",
                    "description": "Código numérico utilizado para la clasificación geográfica.",
                    "items": { "type": "integer" },
                    "class_data": "classification_code"
                },
                "order_status": {
                    "type": "array",
                    "description": "Representación numérica del estado del pedido.",
                    "items": { "type": "integer" },
                    "class_data": "classification_code"
                }
            }
        },
        "measurements_and_metrics": {
            "type": "object",
            "description": "Valores numéricos, incluyendo mediciones científicas y métricas de proporción.",
            "properties": {
                "temperature": {
                    "type": "array",
                    "description": "La temperatura medida, expresada como un número.",
                    "items": { "type": "number" },
                    "class_data": "cientific_measurement"
                },
                "weight": {
                    "type": "array",
                    "description": "El peso de un objeto, expresado como un número.",
                    "items": { "type": "number" },
                    "class_data": "cientific_measurement"
                },
                "hight": {
                    "type": "array",
                    "description": "La altura de un objeto, expresada como un número.",
                    "items": { "type": "number" },
                    "class_data": "cientific_measurement"
                },
                "width": {
                    "type": "array",
                    "description": "El ancho de un objeto, expresada como un número.",
                    "items": { "type": "number" },
                    "class_data": "cientific_measurement"
                },
                "atmospheric_pressure": {
                    "type": "array",
                    "description": "La presión atmosférica, expresada como un número.",
                    "items": { "type": "number" },
                    "class_data": "cientific_measurement"
                },
                "humidity": {
                    "type": "array",
                    "description": "El nivel de humedad, expresada como un número.",
                    "items": { "type": "number" },
                    "class_data": "cientific_measurement"
                },
                "average_score": {
                    "type": "array",
                    "description": "El puntaje promedio de una prueba o rendimiento, expresado como un número.",
                    "items": { "type": "number" },
                    "class_data": "proportion_and_average"
                },
                "percentage_of_sales": {
                    "type": "array",
                    "description": "El porcentaje de ventas, expresado como un número.",
                    "items": { "type": "number" },
                    "class_data": "proportion_and_average"
                },
                "growth_rate": {
                    "type": "array",
                    "description": "La tasa de crecimiento, expresada como un número.",
                    "items": { "type": "number" },
                    "class_data": "proportion_and_average"
                },
                "min_mean_max": {
                    "type": "array",
                    "description": "Una colección de valores numéricos que representan el mínimo, la media y el máximo.",
                    "items": { "type": "number" },
                    "class_data": "proportion_and_average"
                },
                "latitude": {
                    "type": "array",
                    "description": "La coordenada de latitud geográfica.",
                    "items": { "type": "number" },
                    "class_data": "coordenates"
                },
                "longitude": {
                    "type": "array",
                    "description": "La coordenada de longitud geográfica.",
                    "items": { "type": "number" },
                    "class_data": "coordenates"
                }
            }
        },
        "transactions_and_financials": {
            "type": "object",
            "description": "Información relacionada con transacciones, costos y finanzas.",
            "properties": {
                "number_of_units_sold": {
                    "type": "array",
                    "description": "El número total de unidades vendidas.",
                    "items": { "type": "integer" },
                    "class_data": "counted_values"
                },
                "number_of_transactions": {
                    "type": "array",
                    "description": "El número total de transacciones.",
                    "items": { "type": "integer" },
                    "class_data": "counted_values"
                },
                "edad": {
                    "type": "array",
                    "description": "La edad de una persona en años.",
                    "items": { "type": "integer" },
                    "class_data": "counted_values"
                },
                "scores": {
                    "type": "array",
                    "description": "Puntuaciones numéricas, que pueden incluir decimales.",
                    "items": { "type": "number" },
                    "class_data": "counted_values"
                },
                "unit_price": {
                    "type": "array",
                    "description": "El precio de una sola unidad.",
                    "items": { "type": "number" },
                    "class_data": "monetary_values"
                },
                "total_cost": {
                    "type": "array",
                    "description": "El costo total.",
                    "items": { "type": "number" },
                    "class_data": "monetary_values"
                },
                "revenue": {
                    "type": "array",
                    "description": "Los ingresos totales generados.",
                    "items": { "type": "number" },
                    "class_data": "monetary_values"
                },
                "interest_rates": {
                    "type": "array",
                    "description": "La tasa de interés.",
                    "items": { "type": "number" },
                    "class_data": "monetary_values"
                }
            }
        },
        "dates_and_times": {
            "type": "object",
            "description": "Datos de fecha y hora, incluyendo registros de tiempo y eventos.",
            "properties": {
                "record_creation": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha y hora en que se creó un registro.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "date_time_event"
                },
                "transaction_date": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha de una transacción financiera.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "date_time_event"
                },
                "session_start_time": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha y hora en que comenzó una sesión.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "date_time_event"
                },
                "birthdate": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha de nacimiento de un individuo.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "date_time_event"
                },
                "timestamp": {
                    "type": "array",
                    "format": "date-time",
                    "description": "Una fecha y hora específica capturada en un evento.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "sensor_and_time_series"
                },
                "reading_date": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha en que se tomó una lectura o medición.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "sensor_and_time_series"
                },
                "event_time_log": {
                    "type": "array",
                    "format": "date-time",
                    "description": "Un registro de la fecha y hora de un evento.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "sensor_and_time_series"
                },
                "holiday_day": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha de un día festivo.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "calendar"
                },
                "product_expiration_date": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha de vencimiento de un producto.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "calendar"
                },
                "invoice_due": {
                    "type": "array",
                    "format": "date-time",
                    "description": "La fecha de vencimiento de una factura.",
                    "items": { "type": "string", "format": "date-time" },
                    "class_data": "calendar"
                }
            }
        },
        "text_and_unstructured_data": {
            "type": "object",
            "description": "Datos de texto estructurados y no estructurados.",
            "properties": {
                "client_name": {
                    "type": "array",
                    "description": "Contiene datos de texto del nombre de un cliente.",
                    "items": { "type": "string" },
                    "class_data": "text_string"
                },
                "address": {
                    "type": "array",
                    "description": "Contiene datos de texto de una dirección postal.",
                    "items": { "type": "string" },
                    "class_data": "text_string"
                },
                "user_review": {
                    "type": "array",
                    "description": "Contiene datos de texto de una reseña de usuario.",
                    "items": { "type": "string" },
                    "class_data": "text_string"
                },
                "product_description": {
                    "type": "array",
                    "description": "Contiene datos de texto de una descripción del producto.",
                    "items": { "type": "string" },
                    "class_data": "text_string"
                },
                "website_url": {
                    "type": "array",
                    "description": "Contiene datos de texto de una URL de un sitio web.",
                    "items": { "type": "string" },
                    "class_data": "text_string"
                },
                "mix_of_numbers_and_text": {
                    "type": "array",
                    "description": "Contiene una mezcla de números y texto.",
                    "items": { "type": "string" },
                    "class_data": "mixed"
                },
                "raw_data_applied": {
                    "type": "array",
                    "description": "Contiene datos brutos de varias fuentes.",
                    "items": { "type": "string" },
                    "class_data": "mixed"
                },
                "address_and_city": {
                    "type": "array",
                    "description": "Contiene una combinación de dirección y ciudad.",
                    "items": { "type": "string" },
                    "class_data": "people_and_places_id"
                },
                "country": {
                    "type": "array",
                    "description": "Contiene el nombre de un país.",
                    "items": { "type": "string" },
                    "class_data": "people_and_places_id"
                },
                "product_reviews": {
                    "type": "array",
                    "description": "Contenido de texto no estructurado que representa una reseña del producto.",
                    "items": { "type": "string" },
                    "class_data": "free_text"
                },
                "social_media_comments": {
                    "type": "array",
                    "description": "Contenido de texto no estructurado de comentarios de redes sociales.",
                    "items": { "type": "string" },
                    "class_data": "free_text"
                },
                "description_of_log_errors": {
                    "type": "array",
                    "description": "Contenido de texto no estructurado que proporciona una descripción de los errores del registro.",
                    "items": { "type": "string" },
                    "class_data": "free_text"
                }
            }
        },
        "conditions_and_booleans": {
            "type": "object",
            "description": "Datos categóricos y valores booleanos que representan condiciones.",
            "properties": {
                "civil_status": {
                    "type": "array",
                    "description": "El estado civil de un individuo.",
                    "items": { "type": "string" },
                    "class_data": "limited_and_concrete"
                },
                "gender": {
                    "type": "array",
                    "description": "El género de una persona.",
                    "items": { "type": "string" },
                    "class_data": "limited_and_concrete"
                },
                "product_type": {
                    "type": "array",
                    "description": "La categoría o tipo de un producto.",
                    "items": { "type": "string" },
                    "class_data": "categorical_values"
                },
                "payment_method": {
                    "type": "array",
                    "description": "El método utilizado para un pago.",
                    "items": { "type": "string" },
                    "class_data": "categorical_values"
                },
                "brand": {
                    "type": "array",
                    "description": "El nombre de marca de un producto.",
                    "items": { "type": "string" },
                    "class_data": "categorical_values"
                },
                "level_of_education": {
                    "type": "array",
                    "description": "El nivel más alto de educación alcanzado por una persona.",
                    "items": { "type": "string" },
                    "class_data": "limited_and_concrete"
                },
                "product_rating": {
                    "type": "array",
                    "description": "Una calificación numérica dada a un producto.",
                    "items": { "type": "integer" },
                    "class_data": "rating_and_ranks"
                },
                "clothing_size": {
                    "type": "array",
                    "description": "El tamaño de una prenda de vestir.",
                    "items": { "type": "string" },
                    "class_data": "rating_and_ranks"
                },
                "satisfaction_level": {
                    "type": "array",
                    "description": "Un nivel numérico que indica la satisfacción del cliente.",
                    "items": { "type": "integer" },
                    "class_data": "rating_and_ranks"
                },
                "is_null": {
                    "type": "array",
                    "description": "Indica si un valor es nulo.",
                    "items": { "type": "boolean" },
                    "class_data": "columns_from_conditions"
                },
                "detected_error": {
                    "type": "array",
                    "description": "Indica si se detectó un error.",
                    "items": { "type": "boolean" },
                    "class_data": "columns_from_conditions"
                },
                "is_active_client": {
                    "type": "array",
                    "description": "Indica si un cliente está actualmente activo.",
                    "items": { "type": "boolean" },
                    "class_data": "record_states"
                },
                "the_order_has_been_delivered": {
                    "type": "array",
                    "description": "Indica si un pedido se ha entregado con éxito.",
                    "items": { "type": "boolean" },
                    "class_data": "record_states"
                },
                "product_in_stock": {
                    "type": "array",
                    "description": "Indica si un producto está disponible en stock.",
                    "items": { "type": "boolean" },
                    "class_data": "record_states"
                },
                "is_over_18_years_old": {
                    "type": "array",
                    "description": "Indica si una persona es mayor de 18 años.",
                    "items": { "type": "boolean" },
                    "class_data": "logical_comparison"
                },
                "sales_for_the_month_are_higher_than_the_target": {
                    "type": "array",
                    "description": "Indica si las ventas mensuales han superado el objetivo.",
                    "items": { "type": "boolean" },
                    "class_data": "logical_comparison"
                },
                "the_country_is_spain": {
                    "type": "array",
                    "description": "Indica si el país es España.",
                    "items": { "type": "boolean" },
                    "class_data": "logical_comparison"
                }
            }
        },
        "dataframe_package": {
            "type": "object",
            "description": "Contiene los datos estructurados en un formato de dataframe, con filas correlacionadas que agrupan todas las propiedades de un solo evento o registro.",
            "properties": {
                "data": {
                    "type": "array",
                    "description": "Array de objetos, donde cada objeto representa una fila correlacionada del dataframe.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "client_id": { "type": "integer" },
                            "product_id": { "type": "integer" },
                            "order_number": { "type": "integer" },
                            "employee_number": { "type": "integer" },
                            "postal_code": { "type": "integer" },
                            "order_status": { "type": "integer" },
                            "temperature": { "type": "number" },
                            "weight": { "type": "number" },
                            "hight": { "type": "number" },
                            "width": { "type": "number" },
                            "atmospheric_pressure": { "type": "number" },
                            "humidity": { "type": "number" },
                            "average_score": { "type": "number" },
                            "percentage_of_sales": { "type": "number" },
                            "growth_rate": { "type": "number" },
                            "min_mean_max": { "type": "number" },
                            "latitude": { "type": "number" },
                            "longitude": { "type": "number" },
                            "number_of_units_sold": { "type": "integer" },
                            "number_of_transactions": { "type": "integer" },
                            "edad": { "type": "integer" },
                            "scores": { "type": "number" },
                            "unit_price": { "type": "number" },
                            "total_cost": { "type": "number" },
                            "revenue": { "type": "number" },
                            "interest_rates": { "type": "number" },
                            "record_creation": { "type": "string", "format": "date-time" },
                            "transaction_date": { "type": "string", "format": "date-time" },
                            "session_start_time": { "type": "string", "format": "date-time" },
                            "birthdate": { "type": "string", "format": "date-time" },
                            "timestamp": { "type": "string", "format": "date-time" },
                            "reading_date": { "type": "string", "format": "date-time" },
                            "event_time_log": { "type": "string", "format": "date-time" },
                            "holiday_day": { "type": "string", "format": "date-time" },
                            "product_expiration_date": { "type": "string", "format": "date-time" },
                            "invoice_due": { "type": "string", "format": "date-time" },
                            "client_name": { "type": "string" },
                            "address": { "type": "string" },
                            "user_review": { "type": "string" },
                            "product_description": { "type": "string" },
                            "website_url": { "type": "string" },
                            "mix_of_numbers_and_text": { "type": "string" },
                            "raw_data_applied": { "type": "string" },
                            "address_and_city": { "type": "string" },
                            "country": { "type": "string" },
                            "product_reviews": { "type": "string" },
                            "social_media_comments": { "type": "string" },
                            "description_of_log_errors": { "type": "string" },
                            "civil_status": { "type": "string" },
                            "gender": { "type": "string" },
                            "product_type": { "type": "string" },
                            "payment_method": { "type": "string" },
                            "brand": { "type": "string" },
                            "level_of_education": { "type": "string" },
                            "product_rating": { "type": "integer" },
                            "clothing_size": { "type": "string" },
                            "satisfaction_level": { "type": "integer" },
                            "is_null": { "type": "boolean" },
                            "detected_error": { "type": "boolean" },
                            "is_active_client": { "type": "boolean" },
                            "the_order_has_been_delivered": { "type": "boolean" },
                            "product_in_stock": { "type": "boolean" },
                            "is_over_18_years_old": { "type": "boolean" },
                            "sales_for_the_month_are_higher_than_the_target": { "type": "boolean" },
                            "the_country_is_spain": { "type": "boolean" }
                        }
                    }
                }
            },
            "json_output_template": {
                "dataframe_package": {
                    "data": []
                },
                "identifiers_and_codes": {
                    "client_id": [],
                    "product_id": [],
                    "order_number": [],
                    "employee_number": [],
                    "postal_code": [],
                    "order_status": []
                },
                "measurements_and_metrics": {
                    "temperature": [],
                    "weight": [],
                    "hight": [],
                    "width": [],
                    "atmospheric_pressure": [],
                    "humidity": [],
                    "average_score": [],
                    "percentage_of_sales": [],
                    "growth_rate": [],
                    "min_mean_max": [],
                    "latitude": [],
                    "longitude": []
                },
                "transactions_and_financials": {
                    "number_of_units_sold": [],
                    "number_of_transactions": [],
                    "edad": [],
                    "scores": [],
                    "unit_price": [],
                    "total_cost": [],
                    "revenue": [],
                    "interest_rates": []
                },
                "dates_and_times": {
                    "record_creation": [],
                    "transaction_date": [],
                    "session_start_time": [],
                    "birthdate": [],
                    "timestamp": [],
                    "reading_date": [],
                    "event_time_log": [],
                    "holiday_day": [],
                    "product_expiration_date": [],
                    "invoice_due": []
                },
                "text_and_unstructured_data": {
                    "client_name": [],
                    "address": [],
                    "user_review": [],
                    "product_description": [],
                    "website_url": [],
                    "mix_of_numbers_and_text": [],
                    "raw_data_applied": [],
                    "address_and_city": [],
                    "country": [],
                    "product_reviews": [],
                    "social_media_comments": [],
                    "description_of_log_errors": []
                },
                "conditions_and_booleans": {
                    "civil_status": [],
                    "gender": [],
                    "product_type": [],
                    "payment_method": [],
                    "brand": [],
                    "level_of_education": [],
                    "product_rating": [],
                    "clothing_size": [],
                    "satisfaction_level": [],
                    "is_null": [],
                    "detected_error": [],
                    "is_active_client": [],
                    "the_order_has_been_delivered": [],
                    "product_in_stock": [],
                    "is_over_18_years_old": [],
                    "sales_for_the_month_are_higher_than_the_target": [],
                    "the_country_is_spain": []
                },
                "generated_report": {
                    "report_type": None,
                    "variables_and_standards": [],
                    "findings": {
                        "observations": None,
                        "key_points": []
                    }
                }
            }
        }
    }
}