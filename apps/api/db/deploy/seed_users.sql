-- Deploy medicore:seed_users to pg

BEGIN;

INSERT INTO users (email, password_hash, full_name, role, is_active) VALUES
-- 10 Admins
('admin1@medicore.com', '$2b$12$Z7L4.gXv20aclOEUgl6EJu4mm4/wFv1fM48qu7LdxI0KeMxzEDh.W', 'Admin User 1', 'ADMIN', TRUE),
('admin2@medicore.com', '$2b$12$GXK9c5D2Ou/pN9iPMRmlLuw4pGh0fqs0iKn486of2e3XSsXher4SG', 'Admin User 2', 'ADMIN', TRUE),
('admin3@medicore.com', '$2b$12$UlhjH6qSgeE293bnPIEc1eLD5iIrcJWT8vuEikm8lHSo7S5qAeB1O', 'Admin User 3', 'ADMIN', TRUE),
('admin4@medicore.com', '$2b$12$lhA0V15XH/d2.EecuMnv1ueITMS50fnAazhs9C6.Uc1ZGnqrChyzW', 'Admin User 4', 'ADMIN', TRUE),
('admin5@medicore.com', '$2b$12$mps/02s5CAxIpgkpbBBizOdt3IwIn2Q5Syz9VkZ.Z3TQJBCvtpQmC', 'Admin User 5', 'ADMIN', TRUE),
('admin6@medicore.com', '$2b$12$LXF54AzCtUD4MZBt3qlF2edTcWMtsWD2ajiGuOqhswNEDXqqwP//K', 'Admin User 6', 'ADMIN', TRUE),
('admin7@medicore.com', '$2b$12$AdMcdz0cQRwinkJA8Cfu/ORKqpYb86sb/fnKu8qr1WMnl5duMH1Oa', 'Admin User 7', 'ADMIN', TRUE),
('admin8@medicore.com', '$2b$12$qH/p.8ZqS4xcFJGfENWjV.yDzkj1pbHJzNaXNLXeqcCwx0RcIjRBy', 'Admin User 8', 'ADMIN', TRUE),
('admin9@medicore.com', '$2b$12$Tq7xU/vzDp33vRxPZALDGueG5GfcwRQRV0fOe6ujlFOL8XvUNWn9C', 'Admin User 9', 'ADMIN', TRUE),
('admin10@medicore.com', '$2b$12$xl...2XAMLJAtNk7ad7dc.PVFK0xudn9oF4JAptm0hhSyBRHV9jO2', 'Admin User 10', 'ADMIN', TRUE),
-- 10 Doctors
('doctor1@medicore.com', '$2b$12$dtEZz8hitNk6h/q4xy8G/.BP0wBfm6uYKgy6c64Oy58SB2nEoRsBu', 'Doctor User 1', 'DOCTOR', TRUE),
('doctor2@medicore.com', '$2b$12$BRC.GvO6uCpda6X/FKgVxewxDoR8Mhkn.hvxN9VRfS87RsTKwOngW', 'Doctor User 2', 'DOCTOR', TRUE),
('doctor3@medicore.com', '$2b$12$3w1FtGiQB3rl8JsCvJXPkebpfYuqzAR79dZR2/b2PEVCN/SRXr5fe', 'Doctor User 3', 'DOCTOR', TRUE),
('doctor4@medicore.com', '$2b$12$9HJTzR8Dbs0Acei.R5vqLuKAEsikin/eaVoVrOuOkJ/6r4t84CMv6', 'Doctor User 4', 'DOCTOR', TRUE),
('doctor5@medicore.com', '$2b$12$WtvCucPlgrRwFoUDHi9kvOB4J6WHk6QvfevvIeRsVkP3AOCPnbyKi', 'Doctor User 5', 'DOCTOR', TRUE),
('doctor6@medicore.com', '$2b$12$/J40pfTAmowRD3mrOKzkre9tqORfD/iJTrZKRr/LlnNxBpZZoFozO', 'Doctor User 6', 'DOCTOR', TRUE),
('doctor7@medicore.com', '$2b$12$yFAzEdPKUFKpASQmQX5I4OWmHokwASKPdUPtZwkvnHcad9fL1DTb.', 'Doctor User 7', 'DOCTOR', TRUE),
('doctor8@medicore.com', '$2b$12$U4gmQH1yInDwCIlSy1DEn.9vGn0aoWERrRNbJAvKXwfo5wKHmTab2', 'Doctor User 8', 'DOCTOR', TRUE),
('doctor9@medicore.com', '$2b$12$eeJFDPwHV.MDCK9/BA8WpOcK.moct9MFqy3aGpI6Bm6C2cwnnxWvy', 'Doctor User 9', 'DOCTOR', TRUE),
('doctor10@medicore.com', '$2b$12$XJfP1A5MTwn44S/UQos/hONsKt7p3pjrhnG4laThlCxVXQf9vpUTW', 'Doctor User 10', 'DOCTOR', TRUE),
-- 10 Nurses
('nurse1@medicore.com', '$2b$12$dLqE0NSUP2ebDYN8TGyXS.HEbv1Ys3M0C3aIuUysRmZC3J.xP.epa', 'Nurse User 1', 'NURSE', TRUE),
('nurse2@medicore.com', '$2b$12$HzdxPrYVOb13Nciyh5oKTurkbH5dkI9DXKsK3gc9gm8udlKp8iU8O', 'Nurse User 2', 'NURSE', TRUE),
('nurse3@medicore.com', '$2b$12$wTp1eRSWuK9cuFMy7tQoFeiubHMJDNnxcXWLl/W3HmZwKpADoE4r.', 'Nurse User 3', 'NURSE', TRUE),
('nurse4@medicore.com', '$2b$12$p58RaU1giHmSkopzIdt6C.kqPIWtZ/W9AGlvgynm4I.FvnNcseN36', 'Nurse User 4', 'NURSE', TRUE),
('nurse5@medicore.com', '$2b$12$bInBxy3CTBVIkFG.u0QnQ.foLJzXhrz6FZFhmkO1uX0uzkxYZADnG', 'Nurse User 5', 'NURSE', TRUE),
('nurse6@medicore.com', '$2b$12$u8WQSEoFJhtCn.q6y9vF2OqPXjjYGTFCfhi12gTy0iC260jYwiUKS', 'Nurse User 6', 'NURSE', TRUE),
('nurse7@medicore.com', '$2b$12$KL.dBiYoEbnal26QQszxf.smJq2/.7dEYRq7g5lXCHcPNLCtKlQ46', 'Nurse User 7', 'NURSE', TRUE),
('nurse8@medicore.com', '$2b$12$WHlZnRsH1irL6daifeCF6eCo4JqZnTlj2w0/dtSN1KlNXXFIJXKrq', 'Nurse User 8', 'NURSE', TRUE),
('nurse9@medicore.com', '$2b$12$QdH11hp.XObHDsHt1RpUKu4st6PAp430UMziFdZyFuCkJPQWUOWUi', 'Nurse User 9', 'NURSE', TRUE),
('nurse10@medicore.com', '$2b$12$cV0s3AS4oOeEwrzhh3G90.ju5eP68X2Mg5JG6mU4bhx0hKMtUrwou', 'Nurse User 10', 'NURSE', TRUE),
-- 10 Receptionists
('receptionist1@medicore.com', '$2b$12$kpk5q7qvKZ3OBNyTbCXxS.m3kPRNQwari/8jhZSa/A7jhFDmiU54O', 'Receptionist User 1', 'RECEPTIONIST', TRUE),
('receptionist2@medicore.com', '$2b$12$0JOMKnJo9iy9NN2AiZ.H/uTdcAjOaFlFzCQsT4Fgn9irfdrZtvQwO', 'Receptionist User 2', 'RECEPTIONIST', TRUE),
('receptionist3@medicore.com', '$2b$12$eiLPm34lQkPlrcsyyWvCa.7r3Qu1ytBiGd5xEa1a8..x4AkhcV0c2', 'Receptionist User 3', 'RECEPTIONIST', TRUE),
('receptionist4@medicore.com', '$2b$12$CZ5QHbmnbbymc7NySAd1Uu9YXEgc4R451CNkDHteR.XaQdYWtjLWm', 'Receptionist User 4', 'RECEPTIONIST', TRUE),
('receptionist5@medicore.com', '$2b$12$wSYggkOzVvoEY14/5iABV.D48m6zxWwnFcTSQ6/04jNHPkuIx1uT2', 'Receptionist User 5', 'RECEPTIONIST', TRUE),
('receptionist6@medicore.com', '$2b$12$1tyS0OpK0dvKEKNgX.x5cu1e8fN1NKXvBQrn7w2Lbszzw8viE/YrC', 'Receptionist User 6', 'RECEPTIONIST', TRUE),
('receptionist7@medicore.com', '$2b$12$UA1H3a7NH5BoZLYcvRf08uxvrbHkAs36x3jcZhLMHC9IOiqVNxk.2', 'Receptionist User 7', 'RECEPTIONIST', TRUE),
('receptionist8@medicore.com', '$2b$12$T1vE9ZzaFKPvMYrzMgqTr.Fo/FMet.9.jr8wHLRwHt6eGT/2HIniu', 'Receptionist User 8', 'RECEPTIONIST', TRUE),
('receptionist9@medicore.com', '$2b$12$C2W5I.nffPnZ.PB8iY/MN.Kldg2Je/k7uRvmMOsnHkDyHETqJ4iVi', 'Receptionist User 9', 'RECEPTIONIST', TRUE),
('receptionist10@medicore.com', '$2b$12$rMkE2SYycEcI71PjQypZb.Wm0ingXDQ7kijQVHyPeFTiknQf5V5wq', 'Receptionist User 10', 'RECEPTIONIST', TRUE),
-- 10 Billing
('billing1@medicore.com', '$2b$12$1JJtwa6zAv2EYxgW7NBHtuzMWLOw9x63.XBxZgkyAY9CbpHiubfSW', 'Billing User 1', 'BILLING', TRUE),
('billing2@medicore.com', '$2b$12$wvaVCFMjjEQuHBPCKS0/6.4aWfwH0rMHtl0n0438uFQ992M0CcsUO', 'Billing User 2', 'BILLING', TRUE),
('billing3@medicore.com', '$2b$12$g7GgTBe8AE2.6IvP2qF6YOA941oNYAYnnf2gc3zDSEyEprFfqkvQ6', 'Billing User 3', 'BILLING', TRUE),
('billing4@medicore.com', '$2b$12$YSzWuNM32mmU5KXTrkxvduGMCiBhOTXlajhFHXnk9fivbdunJKw.a', 'Billing User 4', 'BILLING', TRUE),
('billing5@medicore.com', '$2b$12$2knE6heZ63qf9EYuOKzPcuNeQ.9c7RJ0qxyKil/ybHAabiW6sKqda', 'Billing User 5', 'BILLING', TRUE),
('billing6@medicore.com', '$2b$12$U98A92vpRG7h1qwebxkh1uW4GuH58HUvlXhjTNA4o7Qe0nMhvhita', 'Billing User 6', 'BILLING', TRUE),
('billing7@medicore.com', '$2b$12$nXbV.cFH3B2Mw.fycMrzSu9rrI/L3kfSU7vZFUiZoftBBu6kvmUSe', 'Billing User 7', 'BILLING', TRUE),
('billing8@medicore.com', '$2b$12$P06Y82j7kJeNh2IEaZBoBumMLsrBkjeAk5ojBj9qICbcxCsjd9HXi', 'Billing User 8', 'BILLING', TRUE),
('billing9@medicore.com', '$2b$12$ngCrM7kdtplNKV1dBFuaYu6Z0CukqY0FGEyLBeZtF00r9Wbhu1IBS', 'Billing User 9', 'BILLING', TRUE),
('billing10@medicore.com', '$2b$12$d0V53EHqz9410.Nfiwtgbewn4yNbZY4LVvVkfSMrFZMwCDIcytBR2', 'Billing User 10', 'BILLING', TRUE),
-- 10 Patients
('patient1@medicore.com', '$2b$12$uG85iIyRONydjQ2cbdOowOEGBr3qCu4fQy9Rzk1B54p5xwYgIDdW.', 'Patient User 1', 'PATIENT', TRUE),
('patient2@medicore.com', '$2b$12$ZvLEK2fdgIIOZe0VcLK9b.Y.mYtKV4fBOnSSSik9klNXiknhTqC3e', 'Patient User 2', 'PATIENT', TRUE),
('patient3@medicore.com', '$2b$12$WhpmxaAq.mEk4uD73vN/7OXZbHXnX8mqUsC/11NgB4Qe46tSdLULq', 'Patient User 3', 'PATIENT', TRUE),
('patient4@medicore.com', '$2b$12$Vm33fNyK9p5SpGIp4Ut1i.TTZkwn2EYB/TXMssQhOFBzk0SNFQZwi', 'Patient User 4', 'PATIENT', TRUE),
('patient5@medicore.com', '$2b$12$Mk7wYMbqKltiXWsQC1mXduLY1x450W5ogsfMTRA23ijJxCwVPspRK', 'Patient User 5', 'PATIENT', TRUE),
('patient6@medicore.com', '$2b$12$7Q.m88sDrPQfdMxYeRPdd.h.oIoO8m6pLcdchfL4xj7MISjHPyAO2', 'Patient User 6', 'PATIENT', TRUE),
('patient7@medicore.com', '$2b$12$ZJ5iqwz4bVnVlaEDk9.WxeycXAkuPLJFWe0H52xnIYPsu59T3UcZ2', 'Patient User 7', 'PATIENT', TRUE),
('patient8@medicore.com', '$2b$12$5BV0ABBo9ixL0DZFuA4Yju4cDQF0RQGfJgW.scna9D7n0NQB1HvUK', 'Patient User 8', 'PATIENT', TRUE),
('patient9@medicore.com', '$2b$12$fRAQxhFappSui18yrFuwfeDBnkLC7jpBFJ8dBpb16YceSpoGhV4XK', 'Patient User 9', 'PATIENT', TRUE),
('patient10@medicore.com', '$2b$12$mCMQJdZ5cMDHAC2UQWuuieVZ2yMkpi.No5kJG62qlXyQy0UNCejXC', 'Patient User 10', 'PATIENT', TRUE);

COMMIT;
