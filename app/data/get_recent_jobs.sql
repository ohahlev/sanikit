WITH cte AS (SELECT j.id AS job_id,j.title,j.position,j.requirement, 
                      j.date_created AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Bangkok' AS job_date_created, 
                      j.last_updated AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Bangkok' AS job_last_updated, 
                      array_to_string(array(SELECT c1.name FROM category c1 WHERE c1.id = c.id),',') as categories, 
                      array_to_string(array(SELECT l1.name FROM location l1 WHERE l1.id = l.id),',') as locations, 
                      array_to_string(array(SELECT t1.name FROM tag t1 JOIN tag_job tj1 ON tj1.tag_id = t1.id  
                      WHERE tj1.job_id = j.id),',') as tags, 
                      array_to_string(array(SELECT co1.name FROM company co1 WHERE co1.id = co.id),',') as companies  
                      FROM job j  
                      LEFT JOIN category_job cj ON cj.job_id = j.id  
                      LEFT JOIN category c      ON cj.category_id = c.id  
                      LEFT JOIN location_job lj ON lj.job_id = j.id  
                      LEFT JOIN location l      ON lj.location_id = l.id  
                      LEFT JOIN tag_job tj      ON tj.job_id = j.id  
                      LEFT JOIN tag t           ON tj.tag_id = t.id  
                      LEFT JOIN company_job coj ON coj.job_id = j.id  
                      LEFT JOIN company co      ON coj.company_id = co.id  
                      WHERE j.deleted IS FALSE  
                      AND j.date_created > CURRENT_TIMESTAMP - (31 || ' DAY')::INTERVAL  
                      GROUP BY j.id, c.id, l.id, co.id, tags, companies)  
                      SELECT * FROM (TABLE cte  
                      ORDER BY job_date_created DESC
                      LIMIT 10 OFFSET 0) sub
                      RIGHT JOIN(SELECT COUNT(*) FROM cte) c(full_count) ON TRUE