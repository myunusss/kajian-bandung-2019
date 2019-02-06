# get recent order by therapist
SELECT to_char(a.invoice_time, 'HH24:MI'::text) AS invoice_time, g.card_no, r.room_no,
array_to_string(ARRAY( SELECT therapist.therapist_name
	FROM arinv_therapist at JOIN therapist ON at.therapist_id = therapist.therapist_id
	WHERE a.arinvoice_id = at.arinvoice_id
	ORDER BY therapist.therapist_name), ', '::text)::character varying(200) AS therapists,
to_char(art.begin_treatment_time, 'HH24:MI'::text) AS begin_time,
to_char(art.end_treatment_time, 'HH24:MI'::text) AS end_time,
i.item_name,
t.class_id as therapist_class_id,
a.arinvoice_id
FROM arinv a
JOIN gcard g ON g.gcard_id = a.gcard_id
JOIN room r ON r.room_id = a.room_id
JOIN arinv_therapist art ON a.arinvoice_id = art.arinvoice_id
JOIN therapist t ON t.therapist_id = art.therapist_id
JOIN item i ON a.treatment_item_id = i.item_id
WHERE a.posted = 0 and art.therapist_id in (select therapist_id from therapist where login_id = 'nissa')
	and art.accept_order_time is null
GROUP BY g.card_no, r.room_no, art.begin_treatment_time, art.end_treatment_time, i.item_name, t.class_id,
	array_to_string(ARRAY( SELECT therapist.therapist_name
          FROM arinv_therapist at
          JOIN therapist ON at.therapist_id = therapist.therapist_id
          WHERE a.arinvoice_id = at.arinvoice_id
          ORDER BY therapist.therapist_name), ', '::text)::character varying(200), a.invoice_time, a.arinvoice_id
order by a.invoice_time
limit 1

# NEXT ORDER
SELECT to_char(a.invoice_time, 'HH24:MI'::text) AS invoice_time, g.card_no, r.room_no,
array_to_string(ARRAY( SELECT therapist.therapist_name
	FROM arinv_therapist at JOIN therapist ON at.therapist_id = therapist.therapist_id
	WHERE a.arinvoice_id = at.arinvoice_id
	ORDER BY therapist.therapist_name), ', '::text)::character varying(200) AS therapists,
to_char(art.begin_treatment_time, 'HH24:MI'::text) AS begin_time,
to_char(art.end_treatment_time, 'HH24:MI'::text) AS end_time,
i.item_name,
t.class_id as therapist_class_id,
a.arinvoice_id
FROM arinv a
JOIN gcard g ON g.gcard_id = a.gcard_id
JOIN room r ON r.room_id = a.room_id
JOIN arinv_therapist art ON a.arinvoice_id = art.arinvoice_id
JOIN therapist t ON t.therapist_id = art.therapist_id
JOIN item i ON a.treatment_item_id = i.item_id
WHERE a.posted = 0 and art.therapist_id in (select therapist_id from therapist where login_id = 'nissa')
	and art.accept_order_time is null
GROUP BY g.card_no, r.room_no, art.begin_treatment_time, art.end_treatment_time, i.item_name, t.class_id,
	array_to_string(ARRAY( SELECT therapist.therapist_name
          FROM arinv_therapist at
          JOIN therapist ON at.therapist_id = therapist.therapist_id
          WHERE a.arinvoice_id = at.arinvoice_id
          ORDER BY therapist.therapist_name), ', '::text)::character varying(200), a.invoice_time, a.arinvoice_id
order by a.invoice_time
offset 1

# BOOKING
SELECT booking.booking_id,
    booking.booking_date,
    to_char(booking.booking_time::interval, 'HH24:MI'::text) AS booking_time,
    booking.guest_name,
    bt.therapist_id
   FROM booking
   inner join booking_therapist bt on booking.booking_id = bt.booking_id
  WHERE booking.booking_date = 'now'::text::date and bt.therapist_id = 172
  ORDER BY booking.booking_date, to_char(booking.booking_time::interval, 'HH24:MI'::text)

# COUNT DURATION PACKAGE
SELECT sum(COALESCE(item.duration::integer, 0)::numeric * ai.quantity) AS sum
FROM arinv_item ai
JOIN item ON ai.item_id = item.item_id
LEFT JOIN arinv ar ON ar.arinvoice_id = ai.arinvoice_id
WHERE ai.arinvoice_id = 28 AND item.item_group_id = 1

# DETAIL ORDER
SELECT to_char(a.invoice_time, 'HH24:MI'::text) AS invoice_time,  (g.card_no || ' - ' || a.guest_name) as guest,
	(r.room_no || ' - ' || rt.type_name)::varchar(100),
	array_to_string(ARRAY( SELECT therapist.therapist_name 
		FROM arinv_therapist at JOIN therapist ON at.therapist_id = therapist.therapist_id 
		WHERE a.arinvoice_id = at.arinvoice_id 
		ORDER BY therapist.therapist_name), ', '::text)::character varying(200) AS therapists,
	case when begin_treatment_time is not  null then to_char(art.begin_treatment_time, 'HH24:MI'::text) else '-' end AS begin_time, 
	case when end_treatment_time is not null then to_char(art.end_treatment_time, 'HH24:MI'::text) else '-' end AS end_time, 
	i.item_name, t.class_id, a.arinvoice_id
	FROM arinv a
	left join gcard g ON g.gcard_id = a.gcard_id 
	left join room r ON r.room_id = a.room_id 
	left join room_type rt on r.room_type_id = rt.room_type_id 
	left JOIN arinv_therapist art ON a.arinvoice_id = art.arinvoice_id 
	left JOIN therapist t ON t.therapist_id = art.therapist_id 
	left JOIN item i ON a.treatment_item_id = i.item_id 
	WHERE a.arinvoice_id = 28 and art.therapist_id in (select therapist_id from therapist where login_id = 'nissa')
	GROUP BY g.card_no, r.room_no, art.begin_treatment_time, art.end_treatment_time, i.item_name, t.class_id, a.arinvoice_id, rt.type_name, 
		therapists, a.invoice_time