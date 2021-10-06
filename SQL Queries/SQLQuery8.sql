USE [SmartChat]
GO

/****** Object:  Table [dbo].[Users]    Script Date: 23-09-2021 19:46:12 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Users](
	[ID] [int] NULL,
	[Username] [varchar](255) NULL,
	[Passwd] [varchar](20) NULL,
	[Email] [varchar](255) NULL,
	[FirstName] [varchar](128) NULL,
	[LastName] [varchar](128) NULL
) ON [PRIMARY]
GO


