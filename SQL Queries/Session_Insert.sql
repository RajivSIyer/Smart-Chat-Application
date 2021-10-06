DECLARE @currtime AS DATETIME;
SET @currtime = GETUTCDATE()
INSERT INTO dbo.SessionLog (SessionID, UID, Start, Expire)
VALUES ('67261bdc-25e6-11ec-a6c2-001a7dda7111', 1, @currtime, DATEADD(MI, 1, @currtime)); 