SELECT json_extract_string('{"order_id":101,"amount":"12.50"}','$.order_id') AS raw_id,
       TRY_CAST(json_extract_string('{"amount":"oops"}','$.amount') AS DECIMAL(12,2)) AS invalid_amount;
