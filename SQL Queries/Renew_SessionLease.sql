DECLARE @currtime AS DATETIME;
SET @currtime = GETUTCDATE()

UPDATE dbo.SessionLog
SET Start = @currtime, Expire = DATEADD(MI, 30, @currtime)
WHERE SessionID = '67261bdc-25e6-11ec-a6c2-001a7dda7115';