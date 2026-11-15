"""T-065 L10: S1 only; stdin SSH, no remote evidence or auth files."""
import base64, datetime, hashlib, json, os, pathlib, subprocess, sys, urllib.request, urllib.error
P = json.loads(base64.b64decode('eyJ0b2NfcGF0aCI6IlJDQSBGbGFzaFRpY2tldC8wIMK3IELhuq90IMSR4bqndSB04bqhaSDEkcOieS90MDY1LWw1LW11Yy1sdWMuanNvbiIsImN1cnJlbnQiOiJSQ0EgRmxhc2hUaWNrZXQvMSDCtyBL4bq/dCBxdeG6oyBoaeG7h24gaMOgbmgiLCJhcmNoaXZlIjoiUkNBIEZsYXNoVGlja2V0LzkgwrcgTMawdSB0cuG7ry9MNCDCtyBC4buZIGLhuqNuIHThuqFtIMK3IDE0LTExIiwibmV3X3RvY19iNjQiOiJleUoxYVdRaU9pSjBNRFkxTFd3MUxXMTFZeTFzZFdNaUxDSnBaQ0k2Ym5Wc2JDd2lkbVZ5YzJsdmJpSTZNU3dpZEdsMGJHVWlPaUpONGJ1bFl5QnM0YnVsWXlCU1EwRWlMQ0owWVdkeklqcGJJbEpEUVNJc0lsUXRNRFkxSWl3aVREVWlMQ0p0ZFdNdGJIVmpJbDBzSW5ScGJXVjZiMjVsSWpvaWRYUmpJaXdpWldScGRHRmliR1VpT21aaGJITmxMQ0p6WTJobGJXRldaWEp6YVc5dUlqbzBNaXdpY21WbWNtVnphQ0k2SWlJc0luUnBiV1VpT25zaVpuSnZiU0k2SW01dmR5MHhhQ0lzSW5Sdklqb2libTkzSW4wc0luUnBiV1Z3YVdOclpYSWlPbnNpYUdsa1pHVnVJanAwY25WbGZTd2lkR1Z0Y0d4aGRHbHVaeUk2ZXlKc2FYTjBJanBiWFgwc0luQmhibVZzY3lJNlczc2lhV1FpT2pFc0luUjVjR1VpT2lKMFpYaDBJaXdpZEdsMGJHVWlPaUpONGJ1bFl5QnM0YnVsWXlCU1EwRWdSbXhoYzJoVWFXTnJaWFFpTENKbmNtbGtVRzl6SWpwN0luZ2lPakFzSW5raU9qQXNJbmNpT2pJMExDSm9Jam96TUgwc0ltOXdkR2x2Ym5NaU9uc2liVzlrWlNJNkltMWhjbXRrYjNkdUlpd2lZMjl1ZEdWdWRDSTZJaU1qSUVObzRidU5iaUJ1eHFGcElHTGh1cTkwSU1TUjRicW5kVnh1WEc0dElDb3FXMDNodTZWaklHemh1NlZqSUZKRFFWMG9MMlF2ZERBMk5TMXNOUzF0ZFdNdGJIVmpLU29xSU9LQWxDREVrR25odTROdElHTGh1cTkwSU1TUjRicW5kUzRnUXVHN21TQmk0YnFqYmlCb2FlRzdoMjRnYU1PZ2JtZzZJSEEzSUNocmFHOWhYMUEzS1N3Z1ZqQTRNaTFXTURZMkswZzRZU0FvWkdWZmVIVmhkQ2tzSUZZd056RXRWakEwTVN0SU9HRWdLSFJvWVhsZmRHaGxLUzRnVStHN2tTQmpZVG9nTWpnZ1kyRWd3NWNnTXlCaTRicWpiaUFvT1NCVUxUQTJNaUFySURFeklHUmxkaklnS3lBMklHUmxkak1wTGlCT1ozWGh1NU51SUdkcFlXOGdaR25odTRkdU9pQlVMVEEyTlNBdklFdzRZaXdnYTJuaHU0TnRJRU5vY205dFpTQk1PR003SUdQaHVxMXdJRzVvNGJxdGRDQXhOUzh4TVM4eU1ESTJMbHh1WEc0dElDb3FXMUpEUVNEaWdKUWdZdUc2bzI0Z3hKSGh1NEVnZUhYaHVxVjBJR04xNGJ1UmFTQldNRGd5WFNndlpDOTBNRFkxTFd3NFlpMXlZMkVwS2lvZzRvQ1VJRU5vNGJ1TmJpQmk0YnFqYmlEaWhwSWdZMkVnNG9hU0lITmxjblpwWTJVZzRvYVNJSFJvWVc4Z2RNT2hZeURpaHBJZ1l1RzZzVzVuSUdObzRidXBibWN1SUZZd09ESWdiTU9nSU1TUjRidUJJSGgxNGJxbGRDQmpkZUc3a1drZ1RXbHVhQ0JqYU9HN2pXNGdibWZEb0hrZ01UUXZNVEV2TWpBeU5qc2dWakEzTVNCc3c2QWdZdUc2bzI0Z2RHaGhlU0IwYU9HNnZ5Qmp3N01neEpIaHVxZDFJSEpoSUdQaHVxRnVhQzRnVStHN2tTQmpZVG9nTWpnZ1kyRWdiZUc3bDJrZ1l1RzZvMjR1SUNvcVNHbmh1NGR1SUdqRG9HNW9LaW83SUhacDRidUhZeUJqYU9HN2pXNGdZdUc2bzI0Z2EyakR0RzVuSUhSb1lYa2dibWRvYWVHN2gyMGdkR2gxSUZRdE1EWTBMMVF0TURZMUxseHVYRzR0SUNvcVcxQm93NkYwSUd6aHVxRnBJR1BEc3lERWtjT2hjQ0REb1c0ZzRvQ1VJRlF0TURZeVhTZ3ZaQzkwTURZMUxXdzRZaTF3YUdGMExXeGhhU2txS2lEaWdKUWdUT0c3bTNBZ3hKSERvWEFndzZGdUlISnB3NnB1WnlCamFHOGdPU0JqWVNCVUxUQTJNanNnTVRrZ1kyRWdaR1YySUdObzRidUpJR2hwNGJ1SGJpQm5hZUc3bTJrZ2FPRzZvVzRnWTJqR3NHRWdZK0c2cFhBZ3hKSERvWEFndzZGdUxpQkR3N2x1WnlCaVlTQmk0YnFqYmlCMnc2QWdNamdnWTJFdUlDb3FTR25odTRkdUlHakRvRzVvS2lvdVhHNWNiaTBnS2lwYlREUWc0b0NVSUZKRFFTQmk0YnVaSUdMaHVxTnVJSFRodXFGdFhTZ3ZaQzkwTURZMUxXdzBMWEpqWVNrcUtpRGlnSlFnY0Rjc0lGWXdNekl0U0RWaUxDQldNRFF4TFZJeExVZ3hZeXRJTldJclNEaHpNVHNnTWpJZ1kyRWdiZUc3bDJrZ1l1RzZvMjRnS0RrZ1ZDMHdOaklnS3lBeE15QmtaWFl5S1M0Z0tpcE14ckIxSUhSeTRidXZJT0tBbENCaTRidVpJR0xodXFOdUlIVGh1cUZ0SUV3MEtpb3NJR3RvdzdSdVp5QnN3NkFnWXVHNm8yNGd4SkhodTRFZ2VIWGh1cVYwSUdOMTRidVJhUzVjYmx4dUxTQXFLbHRNTkNEaWdKUWdjR2pEb1hRZ2JPRzZvV2tnWXVHN21TQmk0YnFqYmlCMDRicWhiVjBvTDJRdmREQTJOUzFzTkMxd2FHRjBMV3hoYVNrcUtpRGlnSlFnUThPNWJtY2dZbUVnWXVHNm8yNGdkT0c2b1cwN0lEa2dZMkVnVkMwd05qSWdZOE96SUd6aHU1dHdJTVNSdzZGd0lNT2hiaUJ5YWNPcWJtY3NJREV6SUdOaElHUmxkaklnWThPeklHZHA0YnViYVNCbzRicWhiaTRnS2lwTXhyQjFJSFJ5NGJ1dklPS0FsQ0JpNGJ1WklHTGh1cU51SUhUaHVxRnRJRXcwS2lvdVhHNWNiaTBnS2lwYlRETWc0b0NVSUhQaHU3RWdZK0c3a1NCMnc2QWdkR2hoYnlCMHc2RmpJRTB4WFNndlpDOTBNRFkxTFhKallTa3FLaURpZ0pRZ1RlRzdrV01nYU9HN2sya2djWFY1SUdkcFlXOGdaR25odTRkdUlHemh1NXR3SUhSb1lXOGdkTU9oWXk0Z1F1RzZvMjQ2SUZBM0lHdG93N05oTGlCVDRidVJJR05oT2lBNUlHTmhJRlF0TURZeUxpQk9aM1hodTVOdUlHZHBZVzhnWkduaHU0ZHVPaUJVTFRBMk5TQXZJRXd6T3lCdVo4T2dlU0F4TXk4eE1TOHlNREkyT3lBcUttekdzSFVnZEhMaHU2OHFLaTVjYmx4dUxTQXFLbHRNTXlEaWdKUWdjR2pEb1hRZ2JPRzZvV2tnWThPeklNU1J3NkZ3SU1PaGJsMG9MMlF2ZERBMk5TMXdhR0YwTFd4aGFTa3FLaURpZ0pRZ1RlRzdrV01nYU9HN2sya2djWFY1SUhSeVlXNW5JSEJvdzZGMElHemh1cUZwTGlCQzRicWpiam9nVURjZ2EyakRzMkV1SUZQaHU1RWdZMkU2SURrZ1kyRWdWQzB3TmpJdUlFNW5kZUc3azI0Z1oybGhieUJrYWVHN2gyNDZJRlF0TURZMUlDOGdURE03SUc1bnc2QjVJREV6THpFeEx6SXdNalk3SUNvcWJNYXdkU0IwY3VHN3J5b3FMbHh1WEc0dElDb3FXMGN5SUdMaHVxTnVJRFlnNG9DVUlIaGxiU0J6NGJ1eElHUGh1NUZkS0M5a0wzSmpZUzFuTWlrcUtpRGlnSlFnVGVHN2tXTWdhT0c3azJrZ2NYVjVJR1JoYzJoaWIyRnlaQ0JITWk0Z1F1RzZvMjQ2SUZBM0lHdG93N05oTGlCVDRidVJJR05oT2lBNUlHTmhJRlF0TURZeUxpQk9aM1hodTVOdUlHZHBZVzhnWkduaHU0ZHVPaUJVTFRBMk1pQXZJRWN4SUdMaHVxTnVJRFk3SUc1bnc2QjVJREV5THpFeEx6SXdNalk3SUNvcWJNYXdkU0IwY3VHN3J5b3FMbHh1WEc0dElDb3FXMGN5SUdMaHVxTnVJRFlnNG9DVUlIQm93NkYwSUd6aHVxRnBJR1BEc3lERWtjT2hjQ0REb1c1ZEtDOWtMM0pqWVMxbk1pMXdhR0YwTFd4aGFTa3FLaURpZ0pRZ1RlRzdrV01nYU9HN2sya2djWFY1SUhCb3c2RjBJR3podXFGcElFY3lMaUJDNGJxamJqb2dVRGNnYTJqRHMyRXVJRlBodTVFZ1kyRTZJRGtnWTJFZ1ZDMHdOakl1SUU1bmRlRzdrMjRnWjJsaGJ5QmthZUc3aDI0NklGUXRNRFl5SUM4Z1J6RWdZdUc2bzI0Z05qc2dibWZEb0hrZ01USXZNVEV2TWpBeU5qc2dLaXBzeHJCMUlIUnk0YnV2S2lvdVhHNWNiaU1qSXlCVWN1RzZvVzVuSUhSb3c2RnBJSGJEb0NCbmFlRzdtMmtnYU9HNm9XNWNibHh1VURjZ3hKSERveUJyYU1PellTNGdWakE0TWlCc3c2QWd4SkhodTRFZ2VIWGh1cVYwSUdOMTRidVJhU0JOYVc1b0lHTm80YnVOYmpzZ1ZqQTNNU0JzdzZBZ1l1RzZvMjRnZEdoaGVTQjBhT0c2dnlCanc3TWd4SkhodXFkMUlISmhJR1BodXFGdWFDNGdTMmpEdEc1bklITjFlU0IyYWVHN2gyTWdZMmpodTQxdUlHTGh1cU51SUd6RG9DQnVaMmhwNGJ1SGJTQjBhSFVnZEdGemF5Qm9iK0c2dDJNZ1l1RzZzVzVuSUdObzRidXBibWNnYUduaHU0ZDFJSEYxNGJxaklIQm94ckRHb1c1bklIQm93NkZ3TGx4dVhHNUlZV2tnYUdGemFDQmo0YnFsY0NCaTRicWpiaUJRTnlCc3c2QWdiblZzYkNCMGNtOXVaeUJqYU9HN2lTQnQ0YnVsWXlCVUxUQTJORHNnYTJqRHRHNW5JSE4xZVNCb1lYTm9JSFRodTZzZ1ptbHNaU0RFa2VHNnAzVWdjbUV1SUZSeVlXNW5JR05vdzYxdWFDQjJ3NkFnYmVHN3BXTWdiT0c3cFdNZ2EyakR0RzVuSUdObzRidXBZU0RFa2NPaGNDRERvVzR1SUZOd1lXNGdiR2x1YXlCdFpYTnpZV2RsSUdOb3hyQmhJR2podTVjZ2RITGh1Nk11WEc1Y2JrNW5kZUc3azI0Z1l1RzZvMjRnZHNPZ0lHTmhPaUJ5WlhOMWJIUnpMMVF0TURZMEwySmhiaTE0ZFdGMEwyTm9hUzF0ZFdNdFltRnVMbXB6YjI0dUlFUGh1NjFoSUhQaHU1VWdkSEpoYm1jZ1kyRTZJRnQwNG9pU016QXdMSFFyTXpBd0tTNGlmWDFkZlFvPSIsIm9sZF90b2NfYjY0IjoiZXdvZ0lDSjFhV1FpT2lBaWREQTJOUzFzTlMxdGRXTXRiSFZqSWl3S0lDQWlhV1FpT2lCdWRXeHNMQW9nSUNKMlpYSnphVzl1SWpvZ01Td0tJQ0FpZEdsMGJHVWlPaUFpVGVHN3BXTWdiT0c3cFdNZ1VrTkJJaXdLSUNBaWRHRm5jeUk2SUZzS0lDQWdJQ0pTUTBFaUxBb2dJQ0FnSWxRdE1EWTFJaXdLSUNBZ0lDSk1OU0lzQ2lBZ0lDQWliWFZqTFd4MVl5SUtJQ0JkTEFvZ0lDSjBhVzFsZW05dVpTSTZJQ0oxZEdNaUxBb2dJQ0psWkdsMFlXSnNaU0k2SUdaaGJITmxMQW9nSUNKelkyaGxiV0ZXWlhKemFXOXVJam9nTkRJc0NpQWdJbkpsWm5KbGMyZ2lPaUFpSWl3S0lDQWlkR2x0WlNJNklIc0tJQ0FnSUNKbWNtOXRJam9nSW01dmR5MHhhQ0lzQ2lBZ0lDQWlkRzhpT2lBaWJtOTNJZ29nSUgwc0NpQWdJblJwYldWd2FXTnJaWElpT2lCN0NpQWdJQ0FpYUdsa1pHVnVJam9nZEhKMVpRb2dJSDBzQ2lBZ0luUmxiWEJzWVhScGJtY2lPaUI3Q2lBZ0lDQWliR2x6ZENJNklGdGRDaUFnZlN3S0lDQWljR0Z1Wld4eklqb2dXd29nSUNBZ2V3b2dJQ0FnSUNBaWFXUWlPaUF4TEFvZ0lDQWdJQ0FpZEhsd1pTSTZJQ0owWlhoMElpd0tJQ0FnSUNBZ0luUnBkR3hsSWpvZ0lrM2h1NlZqSUd6aHU2VmpJRkpEUVNCR2JHRnphRlJwWTJ0bGRDSXNDaUFnSUNBZ0lDSm5jbWxrVUc5eklqb2dld29nSUNBZ0lDQWdJQ0o0SWpvZ01Dd0tJQ0FnSUNBZ0lDQWllU0k2SURBc0NpQWdJQ0FnSUNBZ0luY2lPaUF5TkN3S0lDQWdJQ0FnSUNBaWFDSTZJRE13Q2lBZ0lDQWdJSDBzQ2lBZ0lDQWdJQ0p2Y0hScGIyNXpJam9nZXdvZ0lDQWdJQ0FnSUNKdGIyUmxJam9nSW0xaGNtdGtiM2R1SWl3S0lDQWdJQ0FnSUNBaVkyOXVkR1Z1ZENJNklDSWpJeUJEYU9HN2pXNGdic2FoYVNCaTRicXZkQ0RFa2VHNnAzVmNibHh1TFNBcUtsdE40YnVsWXlCczRidWxZeUJTUTBGZEtDOWtMM1F3TmpVdGJEVXRiWFZqTFd4MVl5a3FLaURpZ0pRZ3hKQnA0YnVEYlNCaTRicXZkQ0RFa2VHNnAzVTdJR05vNGJ1TmJpREVrY082Ym1jZ1pHRnphR0p2WVhKa0lIYkRvQ0J0NGJ1Ull5QnN4ckIxSUhSeTRidXZMaUJDNGJxamJqb2djRGNnS0d0b2IyRmZVRGNwT3lCV01ETXlMVWcxWWlBb1pHVmZlSFZoZENrN0lGWXdOREV0VWpFdFNERmpLMGcxWWl0SU9ITXhJQ2gwYUdGNVgzUm9aU2t1SUZQaHU1RWdZMkU2SURJeUlHTmhJTU9YSURNZ1l1RzZvMjRnYUduaHU0ZHVJR2pEb0c1b0xpQk9aM1hodTVOdUlHZHBZVzhnWkduaHU0ZHVPaUJVTFRBMk5TQXZJRXcxT3lCdVo4T2dlU0F4TkM4eE1TOHlNREkyT3lBcUttaHA0YnVIYmlCb3c2QnVhQ29xTGx4dVhHNHRJQ29xVzFKRFFTRGlnSlFnWTJqaHU0MXVJR0xodXFOdUlFMHhJR1BEdVc1bklHTmhYU2d2WkM5ME1EWTFMV3cwTFhKallTa3FLaURpZ0pRZ1Eyamh1NDF1SUdMaHVxTnVJT0tHa2lCallTRGlocElnYzJWeWRtbGpaU0RpaHBJZ2RHaGhieUIwdzZGaklPS0draUJpNGJxeGJtY2dZMmpodTZsdVp5NGdRdUc2bzI0NklIQTNJQ2hyYUc5aFgxQTNLVHNnVmpBek1pMUlOV0lnS0dSbFgzaDFZWFFwT3lCV01EUXhMVkl4TFVneFl5dElOV0lyU0Roek1TQW9kR2hoZVY5MGFHVXBMaUJUNGJ1UklHTmhPaUF5TWlCallTQW9PU0JVTFRBMk1pQXJJREV6SUdSbGRqSXBMaUJPWjNYaHU1TnVJR2RwWVc4Z1pHbmh1NGR1T2lCVUxUQTJOU0F2SUV3ME95QnVaOE9nZVNBeE5DOHhNUzh5TURJMk95QXFLbWhwNGJ1SGJpQm93NkJ1YUNvcUxseHVYRzR0SUNvcVcxQm93NkYwSUd6aHVxRnBJR1BEc3lERWtjT2hjQ0REb1c0ZzRvQ1VJRlF0TURZeVhTZ3ZaQzkwTURZMUxXdzBMWEJvWVhRdGJHRnBLU29xSU9LQWxDQllaVzBnY21uRHFtNW5JTVNSdzZGd0lNT2hiaURFa2NPaklIVERvV05vSUhOaGRTQnJhR2tnZUdWdElHdmh1cjkwSUhGMTRicWpMaUJDNGJxamJqb2djRGNnS0d0b2IyRmZVRGNwT3lCV01ETXlMVWcxWWlBb1pHVmZlSFZoZENrN0lGWXdOREV0VWpFdFNERmpLMGcxWWl0SU9ITXhJQ2gwYUdGNVgzUm9aU2t1SUZQaHU1RWdZMkU2SURrZ1kyRWdWQzB3TmpJZ1k4T3pJTVNSdzZGd0lNT2hianNnTVRNZ1pHVjJNaUJqYU9HN2lTQmp3N01nWjJuaHU1dHBJR2podXFGdUxpQk9aM1hodTVOdUlHZHBZVzhnWkduaHU0ZHVPaUJVTFRBMk5TQXZJRXcwT3lCdVo4T2dlU0F4TkM4eE1TOHlNREkyT3lBcUttaHA0YnVIYmlCb3c2QnVhQ29xTGx4dVhHNHRJQ29xVzB3eklPS0FsQ0J6NGJ1eElHUGh1NUVnZHNPZ0lIUm9ZVzhnZE1PaFl5Qk5NVjBvTDJRdmREQTJOUzF5WTJFcEtpb2c0b0NVSUUzaHU1RmpJR2podTVOcElIRjFlU0JuYVdGdklHUnA0YnVIYmlCczRidWJjQ0IwYUdGdklIVERvV011SUVMaHVxTnVPaUJRTnlCcmFNT3pZUzRnVStHN2tTQmpZVG9nT1NCallTQlVMVEEyTWk0Z1RtZDE0YnVUYmlCbmFXRnZJR1JwNGJ1SGJqb2dWQzB3TmpVZ0x5Qk1NenNnYm1mRG9Ia2dNVE12TVRFdk1qQXlOanNnS2lwc3hyQjFJSFJ5NGJ1dktpb3VYRzVjYmkwZ0tpcGJURE1nNG9DVUlIQm93NkYwSUd6aHVxRnBJR1BEc3lERWtjT2hjQ0REb1c1ZEtDOWtMM1F3TmpVdGNHaGhkQzFzWVdrcEtpb2c0b0NVSUUzaHU1RmpJR2podTVOcElIRjFlU0IwY21GdVp5QndhTU9oZENCczRicWhhUzRnUXVHNm8yNDZJRkEzSUd0b3c3TmhMaUJUNGJ1UklHTmhPaUE1SUdOaElGUXRNRFl5TGlCT1ozWGh1NU51SUdkcFlXOGdaR25odTRkdU9pQlVMVEEyTlNBdklFd3pPeUJ1WjhPZ2VTQXhNeTh4TVM4eU1ESTJPeUFxS216R3NIVWdkSExodTY4cUtpNWNibHh1TFNBcUtsdEhNaUJpNGJxamJpQTJJT0tBbENCNFpXMGdjK0c3c1NCajRidVJYU2d2WkM5eVkyRXRaeklwS2lvZzRvQ1VJRTNodTVGaklHamh1NU5wSUhGMWVTQmtZWE5vWW05aGNtUWdSekl1SUVMaHVxTnVPaUJRTnlCcmFNT3pZUzRnVStHN2tTQmpZVG9nT1NCallTQlVMVEEyTWk0Z1RtZDE0YnVUYmlCbmFXRnZJR1JwNGJ1SGJqb2dWQzB3TmpJZ0x5QkhNU0JpNGJxamJpQTJPeUJ1WjhPZ2VTQXhNaTh4TVM4eU1ESTJPeUFxS216R3NIVWdkSExodTY4cUtpNWNibHh1TFNBcUtsdEhNaUJpNGJxamJpQTJJT0tBbENCd2FNT2hkQ0JzNGJxaGFTQmp3N01neEpIRG9YQWd3NkZ1WFNndlpDOXlZMkV0WnpJdGNHaGhkQzFzWVdrcEtpb2c0b0NVSUUzaHU1RmpJR2podTVOcElIRjFlU0J3YU1PaGRDQnM0YnFoYVNCSE1pNGdRdUc2bzI0NklGQTNJR3RvdzdOaExpQlQ0YnVSSUdOaE9pQTVJR05oSUZRdE1EWXlMaUJPWjNYaHU1TnVJR2RwWVc4Z1pHbmh1NGR1T2lCVUxUQTJNaUF2SUVjeElHTGh1cU51SURZN0lHNW53NkI1SURFeUx6RXhMekl3TWpZN0lDb3FiTWF3ZFNCMGN1RzdyeW9xTGx4dVhHNGpJeU1nVkhMaHVxRnVaeUIwYU1PaGFTQjJ3NkFnWjJuaHU1dHBJR2podXFGdVhHNWNibEEzSU1TUnc2TWdhMmpEczJFdUlGWXdNekl0U0RWaUlHekRvQ0RFa2VHN2dTQjRkZUc2cFhRZ2RPRzZvVzB1SUZZd05ERXRVakV0U0RGakswZzFZaXRJT0hNeElHekRvQ0JpNGJxamJpQjBhR0Y1SUhSbzRicS9JR1BEc3lERWtlRzZwM1VnY21FZ1krRzZvVzVvT3lCamFNYXdZU0JzdzZBZ1l1RzZvMjRnWTNYaHU1RnBJTVNSdzZNZ2JtZG9hZUc3aDIwZ2RHaDFMbHh1WEc1SVlXa2dhR0Z6YUNCajRicWxjQ0JpNGJxamJpQlFOeUJzdzZBZ2JuVnNiQ0IwY205dVp5QmphT0c3aVNCdDRidWxZeUJVTFRBMk5Ec2dhMmpEdEc1bklITjFlU0JvWVhOb0lIVGh1NnNnWm1sc1pTREVrZUc2cDNVZ2NtRXVJRVJsZGlCaTRicWpiaUF5SUdOb3hyQmhJR1BEc3lERWtjT2hjQ0REb1c0Z3hKSEdzT0c3bzJNZ1krRzZwWEFnWTJodklHZHBZVzhnWkduaHU0ZHVMaUJVY21GdVp5QmphTU90Ym1nZ2RzT2dJRzNodTZWaklHemh1NlZqSUd0b3c3UnVaeUJqYU9HN3FXRWd4SkhEb1hBZ3c2RnVMaUJUY0dGdUlHeHBibXNnYldWemMyRm5aU0JqYU1hd1lTQm80YnVYSUhSeTRidWpMbHh1WEc1T1ozWGh1NU51SUdMaHVxTnVJSGJEb0NCallUb2djbVZ6ZFd4MGN5OVVMVEEyTkM5aVlXNHRlSFZoZEM5amFHa3RiWFZqTFdKaGJpNXFjMjl1TGlCRDRidXRZU0J6NGJ1VklIUnlZVzVuSUdOaE9pQmJkT0tJa2pNd01DeDBLek13TUNrdUlnb2dJQ0FnSUNCOUNpQWdJQ0I5Q2lBZ1hRcDlDZz09IiwiZXhwZWN0ZWQiOnsidDA2NS1sNS1tdWMtbHVjLmpzb24iOnsic2hhMjU2IjoiMmUyZTQyNDE5YTlmNDdiZmIxN2MyNGEzOTAyNzNhYjc5NjExODg0OWI5MGExNzY0Nzg3NDcxMGU3NjQxYzJkYiIsImJ5dGVzIjozMDIyfSwidDA2NS1sNC1yY2EuanNvbiI6eyJieXRlcyI6NjIxNzgsInNoYTI1NiI6IjI3MTQwZjdhNjUyNmZkOWM2OGNiN2Y0NWVmNzllOTJlMDZlYzRlZmUxZmU5Yjg5MjA5M2RiZmM1MjNmYTYxZmIifSwidDA2NS1sNC1waGF0LWxhaS5qc29uIjp7ImJ5dGVzIjoyNjE4Mywic2hhMjU2IjoiYmU5OGUzMmNiODA0MTdhZjBhZTQyNmRmMmExYmU2YWQzOTUzNGYwZjdkZmJkNGJlNDllNjJkMjYzMzM1ODlmOSJ9LCJ0MDY1LWw4Yi1yY2EuanNvbiI6eyJieXRlcyI6MzYyOTIsInNoYTI1NiI6IjEyYWNhZDdkOWNiODBjNTc1NDZkZjMyMmUzYzczZjI5MWMwZDc2OWJhMzUyMDI0MGIzNjQ3M2Q1NTJiZTRhYzEifSwidDA2NS1sOGItcGhhdC1sYWkuanNvbiI6eyJieXRlcyI6MTYwNjksInNoYTI1NiI6ImQxZWQ1YjEwMGJkN2RmNzNlMDk2ZDRiYmE0YWI4ZmM5M2Y4MmZkNDRlNzE3ZWNiMjg3N2JmNTZhMDJjMzQxM2YifX0sIm5ld190b2MiOnsic2hhMjU2IjoiYzUxNzAyMDg1NTlkNjJiMTJhYTk0MjhmN2I5ODhhY2YwNTZlZWQyMTVlNGZhNmYwYjM3MWE2Nzg5MzdlZjc0ZiIsImJ5dGVzIjozMTAxfX0='))
B = pathlib.Path('/opt/flash-ticket-obs/pinned/provisioning/dashboards')
C = 'flash-ticket-obs-grafana'
URL = 'http://10.0.0.215:3000'
UIDS = ['t065-l5-muc-luc','t065-l4-rca','t065-l4-phat-lai','t065-l8b-rca','t065-l8b-phat-lai']
L4 = ['t065-l4-rca.json','t065-l4-phat-lai.json']
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def stop():
    assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists(), 'STOP remote'
def digest(b): return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def filepin(p): return digest(p.read_bytes())
def emit(o): print(json.dumps(o,ensure_ascii=False),flush=True)
def inspect(): return json.loads(subprocess.check_output(['docker','inspect',C]))[0]
def auth_headers():
    env = dict(x.split('=',1) for x in inspect()['Config']['Env'] if '=' in x)
    auth = base64.b64encode((env.get('GF_SECURITY_ADMIN_USER','admin')+':'+env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
    return {'Authorization':'Basic '+auth,'Content-Type':'application/json'}
def api(endpoint,method='GET',timeout=35):
    req=urllib.request.Request(URL+endpoint,headers=auth_headers(),method=method)
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r: return {'http':r.status,'data':json.load(r)}
    except urllib.error.HTTPError as e:
        raw=e.read().decode(errors='replace')
        try: raw=json.loads(raw)
        except ValueError: pass
        return {'http':e.code,'data':raw}
def expected_paths(archived=False):
    paths={'t065-l5-muc-luc.json':B/P['toc_path']}
    for name in L4: paths[name]=B/(P['archive'] if archived else P['current'])/name
    for name in ['t065-l8b-rca.json','t065-l8b-phat-lai.json']: paths[name]=B/P['current']/name
    return paths
def validate(archived=False):
    stop()
    paths=expected_paths(archived)
    actual={name:filepin(p) for name,p in paths.items()}
    expected=dict(P['expected'])
    if archived: expected['t065-l5-muc-luc.json']=P['new_toc']
    mismatches=[name for name in expected if actual[name]!=expected[name]]
    for name in L4:
        other=B/(P['current'] if archived else P['archive'])/name
        if other.exists() or other.is_symlink(): mismatches.append(str(other))
    assert not mismatches, 'PIN_OR_DESTINATION_MISMATCH: '+','.join(mismatches)
    return actual
def inventory(archived=False):
    stop()
    ins=inspect()
    files={str(p):filepin(p) for p in sorted(B.parent.rglob('*')) if p.is_file()}
    compose=B.parents[1]/'compose.json'
    files[str(compose)]=filepin(compose)
    paths=expected_paths(archived)
    actual={name:({'path':str(p),**filepin(p),'uid':json.loads(p.read_bytes())['uid']} if p.is_file() else {'path':str(p),'missing':True}) for name,p in paths.items()}
    search=api('/api/search?limit=1000')
    folder_uids=[x['uid'] for x in search.get('data',[]) if x.get('type')=='dash-folder'] if search['http']==200 else []
    return {'utc':utc(),'stop':False,'files':files,'target_files':actual,
        'archive_destinations':{name:{'path':str(B/P['archive']/name),'exists':(B/P['archive']/name).exists()} for name in L4},
        'machine':{'started_at':ins['State']['StartedAt'],'restart_count':ins['RestartCount'],'status':ins['State']['Status']},
        'health':api('/api/health'),'search':search,'root_folders':api('/api/folders?limit=1000'),
        'folders':{uid:api('/api/folders/'+uid) for uid in folder_uids},
        'dashboards':{uid:api('/api/dashboards/uid/'+uid) for uid in UIDS}}
def move_exclusive(source,dest):
    assert source.is_file() and not source.is_symlink(),str(source)
    assert not dest.exists() and not dest.is_symlink(),str(dest)
    dest.parent.mkdir(parents=True,exist_ok=True)
    os.link(source,dest)  # atomic no-replace creation; preserves inode and bytes
    source.unlink()
stop()
action=sys.argv[1]
if action=='before':
    result=inventory(False)
    result['backup_b64']={name:p.read_bytes().hex() for name,p in expected_paths(False).items() if name in P['expected'] and name not in ['t065-l8b-rca.json','t065-l8b-phat-lai.json']}
    result['backup_encoding']='hex'
    try: validate(False); result['preconditions_passed']=True
    except AssertionError as e: result['preconditions_passed']=False; result['error']=str(e)
    emit(result)
    if not result['preconditions_passed']: sys.exit(3)
elif action=='apply':
    actual=validate(False)
    emit({'utc':utc(),'event':'preconditions_passed','files':actual})
    data=base64.b64decode(P['new_toc_b64']); assert digest(data)==P['new_toc']
    toc=B/P['toc_path']; toc.write_bytes(data)
    emit({'utc':utc(),'event':'toc_replaced','path':str(toc),**filepin(toc)})
    for name in L4:
        stop(); src=B/P['current']/name; dst=B/P['archive']/name
        assert filepin(src)==P['expected'][name]
        move_exclusive(src,dst)
        emit({'utc':utc(),'event':'moved','from':str(src),'to':str(dst),**filepin(dst)})
    validate(True)
    emit({'utc':utc(),'event':'apply_complete','restart_by_agent':False})
elif action=='after':
    result=inventory(True)
    try: validate(True); result['file_postconditions_passed']=True
    except AssertionError as e: result['file_postconditions_passed']=False; result['error']=str(e)
    emit(result)
elif action=='render':
    endpoint='/render/d-solo/t065-l5-muc-luc?orgId=1&panelId=1&width=1500&height=1800&tz=UTC'
    req=urllib.request.Request(URL+endpoint,headers=auth_headers())
    try:
        with urllib.request.urlopen(req,timeout=40) as r:
            data=r.read(); emit({'utc':utc(),'endpoint':endpoint,'http':r.status,'content_type':r.headers.get('Content-Type'),'image_b64':base64.b64encode(data).decode(),**digest(data)})
    except urllib.error.HTTPError as e: emit({'utc':utc(),'endpoint':endpoint,'http':e.code,'content_type':e.headers.get('Content-Type'),'body':e.read().decode(errors='replace')})
    except Exception as e: emit({'utc':utc(),'endpoint':endpoint,'error_type':type(e).__name__,'error':str(e)})
elif action=='rollback':
    actual=validate(True)
    emit({'utc':utc(),'event':'rollback_preconditions_passed','files':actual})
    for name in L4: move_exclusive(B/P['archive']/name,B/P['current']/name)
    data=base64.b64decode(P['old_toc_b64']); assert digest(data)==P['expected']['t065-l5-muc-luc.json']
    (B/P['toc_path']).write_bytes(data)
    validate(False)
    emit({'utc':utc(),'event':'rollback_complete','restart_by_agent':False})
else: raise ValueError('Unknown action')
