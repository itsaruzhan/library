----------1 TRIGGER-----------------

create trigger decrease_copy
after INSERT 
on library_bookreturnrecords 
for each row 
begin
update library_book set copies = copies - 1 where book_id = :new.book_id_id;
end;

----------2 TRIGGER-----------------

create or replace trigger increase_copy
after UPDATE 
on library_bookreturnrecords 
for each row 
begin
update library_book set copies = copies + 1 where book_id = :new.book_id_id and :old.returned = 0 and :new.returned = 1 ;
end;

----------3 TRIGGER-----------------

create or replace TRIGGER available_or_not
after UPDATE or Insert
on library_bookreturnrecords 
FOR EACH ROW
   declare copy_num number;
BEGIN
   select library_book.copies into copy_num from library_book
   where  book_id = :new.book_id_id;
    IF copy_num = 1 then
     update library_book set available = 0 ;
    ELSE
     update library_book set available = 1 ;
    END IF;
    END;
    
----------4 TRIGGER AND TRANSACTION-----------------
create or replace trigger set_new_rating
after insert on library_bookrating
for each row
declare 
  pragma autonomous_transaction;

begin 
   update library_store set rating = :new.rating where book_id = :new.book_id;
   commit;
end;

----------5 TRIGGER-----------------

create or replace trigger calc_Rating
    after insert on library_bookrating
Declare
     CURSOR averages
      IS SELECT AVG(lbr.rating) average, lbr.book_id b_id
     from library_book lb, library_bookrating lbr 
     where lb.book_ID = lbr.book_id group by lbr.book_id;
begin
    FOR a IN averages
LOOP
    update library_book 
     set average_Rating = a.average
     where library_book.book_ID = a.b_id;
END LOOP;
    end;
    
----------6 TRIGGER-----------------

Create or Replace trigger user_debt_insert after insert on library_bookreturnedrecord
for each row
declare
u_id library_userdebt.user_id%type;
begin
select user_id into u_id from library_student where library_student.stud_id=:new.stud_id_id;
insert into library_userdebt(cost,days, paid,user_id, book_info_id) values(0, 0, 0,u_id,:new.borrower_id );
end;

----------7 TRIGGER-----------------

create or replace trigger calc_debt
    after insert on library_login
    for each row
declare
    CURSOR days_of_returning
      IS SELECT lbr.book_id_id b_id, lbr.borrower_id bor_id,  (extract(day from sysdate) - extract(day from lbr.due_date)) day_of_returning
     from library_bookreturnedrecord lbr, library_student ls
     where lbr.stud_id_id = ls.stud_id and ls.user_id =:new.user_id  ; 
     dor days_of_returning%ROWTYPE;
begin
   OPEN days_of_returning;
   LOOP 
      FETCH days_of_returning INTO dor;
      EXIT WHEN days_of_returning%NOTFOUND;
      IF days_of_returning%FOUND THEN
        if dor.day_of_returning>0 then
     Update library_userdebt set cost = dor.day_of_returning*100, days = dor.day_of_returning where book_info_id=dor.bor_id ;
       END IF;
       END IF;
    END LOOP;     
    ClOSE  days_of_returning;       
exception
       when no_data_found then
         dbms_output.put_line('he/She is not a student');
end;

----------1 PROCEDURE-----------------

Create or Replace procedure user_action
(user_id In number)
is
a_date DATE := trunc(SYSDATE);
begin
insert into library_login(action,action_date, user_id) values(1, a_date, user_id );
end;


----------2 PROCEDURE-----------------

CREATE OR REPLACE PROCEDURE list_a_rating(in_rating IN Decimal)
AS matching_title VARCHAR2(50);
   TYPE my_cursor IS REF CURSOR;
   the_cursor my_cursor;
BEGIN
  OPEN the_cursor
    FOR 'SELECT title FROM library_book WHERE AVERAGE_RATING =: in_rating'
    USING in_rating;
  DBMS_OUTPUT.PUT_LINE('All books with a rating of '  in_rating  ':');
  LOOP
    FETCH the_cursor INTO matching_title;
    EXIT WHEN the_cursor%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE(matching_title);
  END LOOP;
  CLOSE the_cursor;
END list_a_rating;

EXECUTE list_a_rating(3.1);

    

----------1 FUNCTION-----------------

create or replace function calculate_year(student_id in number)
return NUMBER is 
    start_year number;
    course number;
cursor get_course is select course from library_student where stud_id = student_id;
begin
     open get_course;
     fetch get_course into course;
     close get_course;
     start_year := extract(year from sysdate) - course;
     return start_year;
end;
set serveroutput on;
begin
   dbms_output.put_line(calculate_year(2));
end;


----------2 FUNCTION-----------------

create or replace function show_debt(u_id in number)
return NUMBER is 
u_debt number;
cursor u_debts is  select cost from library_userdebt where user_id = u_id;
begin
     open u_debts;
   fetch u_debts into u_debt ;

   if u_debts%notfound then
      u_debt:= 0;
   end if;

   close u_debts;
   return u_debt;
end;



----------1 TRANSACTION-----------------

declare
  v1_book_id library_book.book_id%type;
  v1_title library_book.title%type;
  v1_edition library_book.edition%type;
  v1_author library_book.author%type;
  v2_id library_bookrating.id%type;
  v3_stud_id_id library_bookreturnedrecord.stud_id_id%type;
  v2_rating library_bookrating.rating%type;
cursor get_data is     
    select t.book_id, t.title, t.edition, t.author,a.id,b.stud_ID_ID,a.rating into v1_book_id, v1_title, v1_edition, v1_author, v2_id, v3_stud_id_id, v2_rating from Library_book t join Library_bookrating a on t.book_id=a.book_id  join Library_bookreturnedrecord b on a.book_id=b.book_id_id where available= 1; 

begin
    open get_data;
    fetch get_data into v1_book_id, v1_title, v1_edition, v1_author, v2_id, v3_stud_id_id, v2_rating;
    close get_data;
    insert into library_store(book_id, title, edition, author, rating_id, stud_id_id, rating) values(v1_book_id, v1_title, v1_edition, v1_author, v2_id, v3_stud_id_id, v2_rating);
update library_book set on_store = 1 where library_book.book_id = v1_book_id;
COMMIT;
end;



