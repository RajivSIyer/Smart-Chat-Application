DECLARE @currtime AS DATETIME;
SET @currtime = GETUTCDATE()

DELETE FROM dbo.SessionLog WHERE Expire < @currtime;